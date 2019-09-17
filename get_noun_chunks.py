import re
import pickle
import spacy
import json
import string

from tqdm import tqdm

class Pdf():

	def __init__(self, file_name = 'data.json'):


		self.file_name = file_name
		self.nlp = spacy.load('en_core_web_sm')

		self.remove_list =[ '(i)','(I)','(II)','(v)','(iv)','(iii)','(ii)','\xad', 
							'(vi)','(vii)','(viii)','\n','\t']

		for i in string.ascii_letters: 

			self.remove_list.append('('+str(i)+')')					
		
		self.punct_list = ["-","%",":","—",";","+",")","(",'"','”']

		self.regex_punct = re.compile('[%s]' % re.escape(''.join(self.punct_list)))					

		self.new_paragraph_concepts = []

		self.paragraph_concepts =[]
		
		self.extract_text()
		self.find_chunks()
		self.extract_nouns()
		self.get_results()
		self.nlp = []

	def remove_multi_space(self, sentence):

		return re.sub(' +',' ',sentence)
	
	def apply_punct_regex(self, sentence):

		sentence = self.regex_punct.sub(' ', sentence)

		return self.remove_multi_space(sentence)
	
	def remove_numbers(self, sentence):

		return re.sub(r'[0-9]+', '', sentence)				

	def remove_bullets(self, sentence):

		for i in self.remove_list:

			sentence = sentence.replace(i,' ')

		return self.remove_multi_space(sentence)


	def extract_text(self):

		with open(self.file_name) as h:
			
			self.json_data = json.load(h)	


		self.text_data=[]

		for idx1, i in enumerate(self.json_data['sections']):

			for idx2,j in enumerate(self.json_data['sections'][idx1]['sections']):

				text1 = str(self.json_data['sections'][idx1]['sections'][idx2]['text'])

				text1 = self.remove_bullets(text1)

				self.text_data.append(text1)


	def add_to_list(self, sentence):

		
		sentence = sentence.strip()

		sentence = self.apply_punct_regex(sentence)

		sentence = self.remove_numbers(sentence)

		sentence = sentence.strip().title()

		if sentence.endswith('.'):
			
			sentence = sentence[:-1]

		if len(sentence)>1:	

			return sentence.strip().title()


	def extract_nouns(self):


		for i in tqdm(self.paragraph_concepts, "Extracting NPs...."):

			temp = []

			for k in i:

				sent = self.nlp(str(k))

				sentence = ""

				for j in sent:

					if str(j.pos_) == 'NOUN' or str(j.pos_) == 'PROPN':
		
						sentence += str(j.text) + " "
					
					else:

						if sentence != "":
							
							chunk = self.add_to_list(sentence)

							temp.append(chunk)
							
							sentence = ""
								

				if sentence != "":

					chunk = self.add_to_list(sentence)

					temp.append(chunk)

			self.new_paragraph_concepts.append(list(set(temp)))

			
	def find_chunks(self):


		for i in tqdm(self.text_data, desc = "Finding Chunks..."):

			text = re.sub('\s+', ' ', i)

			spacy_text = self.nlp(text)

			temp = []

			for j in spacy_text.noun_chunks:

				temp.append(j.text)	

			self.paragraph_concepts.append(temp)	
		
	def get_results(self):

		f=open('concepts2','w')

		for i,j in zip(self.new_paragraph_concepts, self.text_data):

			f.write(str(j)+'\n')
			f.write(str(i)+'\n\n')
		

		f.close()


if __name__ == "__main__":


	pdf_document = Pdf()

	with open("save_new.pickle",'wb') as h:

		pickle.dump(pdf_document, h)

