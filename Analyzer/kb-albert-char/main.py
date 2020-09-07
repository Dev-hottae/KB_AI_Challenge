# from transformers import AlbertModel
# from tokenization_kbalbert import KbAlbertCharTokenizer

kb_albert_model_path = '/home/lab10/JJC/KB_AI_Challenge/Analyzer/model'

# # Load Tokenizer and Model
# tokenizer = KbAlbertCharTokenizer.from_pretrained(kb_albert_model_path)  
# pt_model = AlbertModel.from_pretrained(kb_albert_model_path)

# # inference text input to sentence vector of last layer
# text = '방카슈랑스는 금융의 겸업화 추세에 부응하여 금융산업의 선진화를 도모하고 금융소비자의 편익을 위하여 도입되었습니다.'
# pt_inputs = tokenizer(text, return_tensors='pt')
# pt_outputs = pt_model(**pt_inputs)[0]
# print(pt_outputs)

from transformers import TFAlbertModel

# tokenization_kbalbert.py 파일 경로
from examples.tokenization_kbalbert import KbAlbertCharTokenizer

# Load Tokenizer
tokenizer = KbAlbertCharTokenizer.from_pretrained(kb_albert_model_path)

# Load Model from pytorch checkpoint
tf_model = TFAlbertModel.from_pretrained(kb_albert_model_path, from_pt=True)

# inference text input to sentence vector of last layer
text = '방카슈랑스는 금융의 겸업화 추세에 부응하여 금융산업의 선진화를 도모하고 금융소비자의 편익을 위하여 도입되었습니다.'
tf_inputs = tokenizer(text, return_tensors='tf')
tf_outputs = tf_model(tf_inputs)[0]
print(tf_outputs)