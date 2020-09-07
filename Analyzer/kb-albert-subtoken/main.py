import torch
from noun_splitter import NounSplitter
from transformers import AlbertTokenizer, AlbertModel

# Load noun-splitter 
noun_splitter = NounSplitter("/home/lab10/JJC/KB_AI_Challenge/Analyzer/model/np2.crfsuite")

# ALBERT 모델 종류
# almo = 'albert-base-v1'
# almo = 'albert-large-v1'
# almo = 'albert-xlarge-v1'
# almo = 'albert-xxlarge-v1'
# almo = 'albert-base-v2'
# almo = 'albert-large-v2'
# almo = 'albert-xlarge-v2'
# almo = 'albert-xxlarge-v2'

# KB 모델 학습하면 저장되는데 그거 꺼내서 쓰면 될듯

# Load pre-trained model tokenizer (vocabulary)
tokenizer = AlbertTokenizer.from_pretrained('model-name')

# Load pre-trained model
kb_albert = AlbertModel.from_pretrained('model-name')


# Tokenize inputs
text = "나는 국민은행에서 오픈한 알버트를 쓴다."
tokenized_text = noun_splitter.do_split(text)
input_ids = tokenizer.encode(tokenized_text)

# Convert inputs to PyTorch tensors
input_tensors = torch.tensor([input_ids])

# Predict hidden states features for each layer
with torch.no_grad():
    outputs = kb_albert(input_tensors)
    last_layer = outputs[0]

print(outputs)