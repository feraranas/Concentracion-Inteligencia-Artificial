# References: https://www.youtube.com/watch?v=Rqh4SRcZuDA
import torch
import torch.nn as nn
import torch.optim as optim
import spacy

class CBOW(nn.Module):
     def __init__(self, embedding_size=100, vocab_size=-1):
          super().__init__()
          self.embeddings = nn.Embedding(vocab_size, embedding_size)
          self.linear = nn.Linear(embedding_size, vocab_size)

     def forward(self, inputs):
          # inputs: batch_size x 4 x 100
          embeddings = self.embeddings(inputs).mean(1).squeeze(1) # batch_size x 100
          return self.linear(embeddings)
     
     # In reality we should have a class, and iterate and load it on demand
     # In reality we would load with torch.text (efficient)
     # Create a class for the data loading
     def create_dataset():
          # read text file raw_text.txt as utf-8 in a string
          with open('raw_text.txt', 'r', encoding='utf-8') as f:
               raw_text = f.read()

          # create spacy nlp object
          # tokenize raw_text with spacy
          nlp = spacy.load('en_core_web_sm')
          tokenized_text = [token.text for token in nlp.tokenizer(raw_text)]
          vocab = set(tokenized_text)

          # create word to index and index to word mapping
          word_to_index = {word: i for i, word in enumerate(vocab)}
          index_to_word = {i: word for i, word in enumerate(vocab)}

          # generate training data with two words as context and two words after as target
          data = []
          for i in range(2, len(tokenized_text) - 2):
               context = [
                    tokenized_text[i - 2],
                    tokenized_text[i - 1],
                    tokenized_text[i + 1],
                    tokenized_text[i + 2],
               ]
               target = tokenized_text[i]

               # map context and target to indices and append to data
               context_indices = [word_to_index[word] for word in context]
               target_index = word_to_index[target]
               data.append((context_indices, target_index))               
          
          return data, word_to_index, index_to_word
     
def main():
     EMBEDDING_SIZE = 100
     data, word_to_index, index_to_word = CBOW.create_dataset()
     loss_func = nn.CrossEntropyLoss()
     net = CBOW(embedding_size=EMBEDDING_SIZE, vocab_size=len(word_to_index))
     optimizer = optim.Adam(net.parameters(), lr=0.001)

     # ex[0]: context_indices, ex[1]: target_index
     context_data = torch.tensor([ex[0] for ex in data])
     labels = torch.tensor([ex[1] for ex in data])

     # Create dataset from tensors x,y and dataloader
     dataset = torch.utils.data.TensorDataset(context_data, labels)
     dataloader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)

     # Train the CBOW model
     for epoch in range(100):
          for i, (context, label) in enumerate(dataloader):
               optimizer.zero_grad()
               output = net(context)
               loss = loss_func(output, label)
               loss.backward()
               optimizer.step()

               if i % 100 == 0:
                    print(f'Epoch {epoch} - Batch {i} - Loss: {loss.item()}')

if __name__ == '__main__':
     main()