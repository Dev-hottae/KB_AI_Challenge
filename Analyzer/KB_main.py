# 모델 학습
import json
import logging
import os
import sys
sys.path.insert(0, os.path.abspath('../'))

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import numpy as np
from transformers import (
    AlbertConfig,
    AlbertForSequenceClassification,
    EvalPrediction,
    HfArgumentParser,
    Trainer,
    TrainingArguments,
    set_seed,
)
from kbpack.tokenization_kbalbert import KbAlbertCharTokenizer
from kbpack.utils_finance import FinanceDataset, Split, get_label

logger = logging.getLogger(__name__)



@dataclass
class ModelArguments:
    """
    Arguments pertaining to which model/config/tokenizer we are going to fine-tune from.
    """

    model_name_or_path: str = field(
        metadata={"help": "Path to pretrained model or model identifier from huggingface.co/models"}
    )
    config_name: Optional[str] = field(
        default=None, metadata={"help": "Pretrained config name or path if not the same as model_name"}
    )
    tokenizer_name: Optional[str] = field(
        default=None, metadata={"help": "Pretrained tokenizer name or path if not the same as model_name"}
    )


@dataclass
class DataTrainingArguments:
    """
    Arguments pertaining to what data we are going to input our model for training and eval.
    """

    data_dir: str = field(
        metadata={"help": "The input data dir. Should contain the .txt files for NSMC dataset."}
    )
    labels: Optional[str] = field(
        default=None,
        metadata={"help": "Path to a file containing all labels. If not specified, NSMC labels are used."},
    )
    max_seq_len: int = field(
        default=128,
        metadata={
            "help": "The maximum total input sequence length after tokenization. Sequences longer "
            "than this will be truncated, sequences shorter will be padded."
        },
    )
    overwrite_cache: bool = field(
        default=False, metadata={"help": "Overwrite the cached training and evaluation sets"}
    )


def main(path, epochs=3, batch_size=16, save_steps=5000, text_line=1, label_line=2):

    config_path = path + '/finance_data/finance_config.json'

    # path 를 통해 config 파일 개인에게 맞게 수정
    with open(config_path, "r") as jsonFile:
        data = json.load(jsonFile)

    data["data_dir"] = path + '/finance_data'
    data["model_name_or_path"] = path + '/model'
    data["output_dir"] = path + '/model_outputs'
    data["num_train_epochs"] = epochs
    data["per_device_train_batch_size"] = batch_size
    data["save_steps"] = save_steps

    with open(config_path, "w") as jsonFile:
        json.dump(data, jsonFile)

    parser = HfArgumentParser((ModelArguments, DataTrainingArguments, TrainingArguments))
    model_args, data_args, training_args = parser.parse_json_file(json_file=config_path)
    # if len(sys.argv) == 2 and sys.argv[1].endswith(".json"):
    #     # If we pass only one argument to the script and it's the path to a json file,
    #     # let's parse it to get our arguments.
    #     model_args, data_args, training_args = parser.parse_json_file(json_file=os.path.abspath(sys.argv[1]))
    # else:
    #     model_args, data_args, training_args = parser.parse_args_into_dataclasses()

    if (
        os.path.exists(training_args.output_dir)
        and os.listdir(training_args.output_dir)
        and training_args.do_train
        # output overwrite
        and training_args.overwrite_output_dir
    ):
        raise ValueError(
            f"Output directory ({training_args.output_dir}) already exists and is not empty. Use --overwrite_output_dir to overcome."
        )

    # Setup logging
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO if training_args.local_rank in [-1, 0] else logging.WARN,
    )
    logger.warning(
        "Process rank: %s, device: %s, n_gpu: %s, distributed training: %s, 16-bits training: %s",
        training_args.local_rank,
        training_args.device,
        training_args.n_gpu,
        bool(training_args.local_rank != -1),
        training_args.fp16,
    )
    logger.info("Training/evaluation parameters %s", training_args)

    set_seed(training_args.seed)

    labels = get_label()
    label_map = {i: label for i, label in enumerate(labels)}
    num_labels = len(labels)

    config = AlbertConfig.from_pretrained(
        model_args.config_name if model_args.config_name else model_args.model_name_or_path,
        num_labels=num_labels, id2label=label_map)
    tokenizer = KbAlbertCharTokenizer.from_pretrained(
        model_args.config_name if model_args.config_name else model_args.model_name_or_path,)
    model = AlbertForSequenceClassification.from_pretrained(
        model_args.config_name if model_args.config_name else model_args.model_name_or_path, config=config)

    train_dataset = (
        FinanceDataset(
            data_dir=data_args.data_dir,
            tokenizer=tokenizer,
            max_seq_len=data_args.max_seq_len,
            overwrite_cache=data_args.overwrite_cache,
            mode=Split.train,
            text_line=text_line,
            label_line=label_line
        )
        if training_args.do_train
        else None
    )

    eval_dataset = (
        FinanceDataset(
            data_dir=data_args.data_dir,
            tokenizer=tokenizer,
            max_seq_len=data_args.max_seq_len,
            overwrite_cache=data_args.overwrite_cache,
            mode=Split.test,
            text_line=text_line,
            label_line=label_line
        )
        if training_args.do_eval
        else None
    )

    def align_predictions(predictions: np.ndarray, label_ids: np.ndarray) -> Tuple[List[int], List[int]]:
        preds = np.argmax(predictions, axis=1)

        return preds, label_ids

    def compute_metrics(p: EvalPrediction) -> Dict:
        preds_list, out_label_list = align_predictions(p.predictions, p.label_ids)
        return {
            'acc': (preds_list == out_label_list).mean()
        }

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        compute_metrics=compute_metrics
    )

    if training_args.do_train:
        trainer.train(
            model_path=model_args.model_name_or_path if os.path.isdir(model_args.model_name_or_path) else None
        )
        trainer.save_model(training_args.output_dir)
        tokenizer.save_pretrained(training_args.output_dir)

    results = {}
    if training_args.do_eval:
        logger.info("*** Evaluate ***")

        result = trainer.evaluate()

        output_eval_file = os.path.join(training_args.output_dir, "eval_results.txt")
        with open(output_eval_file, "w") as writer:
            logger.info("***** Eval results *****")
            for key, value in result.items():
                logger.info("  %s = %s", key, value)
                writer.write("%s = %s\n" % (key, value))

        results.update(result)

    return results


def _mp_fn(index):
    main()

if __name__ == "__main__":

    # 기본경로 설정
    path = r'C:\Users\dlagh\PycharmProjects\KB_AI_Challenge\Analyzer'

    # data 는 finance_data 디렉토리 아래 ooo_train.txt, ooo_test.txt 이름으로 저장
    main(path, epochs=3, batch_size=16, save_steps=5000, text_line=2, label_line=3)
