# Name: Hanhong Lu & Zhe Chen & Chenxing Wu
# Description: Implement a Naive Bayes Cllassifier that
# analyzes the sentiment conveyed in text.
#

import math, os, pickle, re

class Bayes_Classifier:

   def __init__(self):
      """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
      cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
      the system will proceed through training.  After running this method, the classifier 
      is ready to classify input text."""
      self.pos_dict = {}
      self.neg_dict = {}
      try:
         self.pos_dict = self.load("positive_dict.txt")
         self.neg_dict = self.load("negative_dict.txt")
      except:
         self.train()

   def train(self):   
      """Trains the Naive Bayes Sentiment Classifier."""
      # First, get the names of all the files in "reviews" directory
      # and stores them in IFileList
      IFileList = []
      for fFileObj in os.walk("reviews/"):
         IFileList = fFileObj[2]
         break
      del IFileList[0];
      self.train_dict(IFileList, self.neg_dict, self.pos_dict)
      self.save(self.pos_dict, "positive_dict.txt")
      self.save(self.neg_dict, "negative_dict.txt")

   def train_dict(self, fileList, neg_dict, pos_dict):
      for fname in fileList:
         # parse each file name
         # print len(fileList);
         title = fname[:-4];
         titles = title.split("_");
         # print fname;
         rank = titles[1];
         content = self.loadFile(fname, "reviews/")
         words = self.tokenize(content)
         if int(rank) < 5:
            # update word frequency in negative dict
            for word in words:
               if neg_dict.has_key(word): # word already exists
                  neg_dict[word] += 1
               else: # new word
                  neg_dict[word] = 1               
         elif int(rank) > 6: # rank == 5
            # update word frequency in positive dict
            for word in words:
               if pos_dict.has_key(word): # word already exists
                  pos_dict[word] += 1
               else: # new word
                  pos_dict[word] = 1 

   def classify(self, sText):
      """Given a target string sText, this function returns the most likely document
      class to which the target string belongs (i.e., positive, negative or neutral).
      """
      n_positive = len(self.pos_dict) + 1 # add one smoothing
      # print "numbr of positive " + str(n_positive)
      n_negative = len(self.neg_dict) + 1 # add one smoothing
      # print "numbr of negative " + str(n_negative)
      p_pos = float(n_positive) / (n_positive+n_negative)
      p_neg = float(n_negative) / (n_positive+n_negative)
      # calculate the sum of the logs of the probilities to avoid underflow
      # p_pos_fs = math.log(p_pos)
      # p_neg_fs = math.log(p_neg)
      p_pos_fs = 0.0
      p_neg_fs = 0.0
      # parse input text
      features = self.tokenize(sText)
      for feature in features:
         # calculate P(positive|fs) by adding the log of P(f|positive)
         try:
            n_f_pos = self.pos_dict[feature] + 1
         except: # word does not exist in dict, # of (feature and positive) = 1 (smoothing)
            n_f_pos = 1
         # print "number of " + feature + " in positive " + str(n_f_pos)
         p_f_pos = float(n_f_pos) / (n_positive+n_negative)
         # print "debug: # of feature that is positive " + str(n_f_pos) + "; # of positive " + str(n_positive) 
         p_f_pos = float(p_f_pos) / p_pos
         p_pos_fs = p_pos_fs + math.log(p_f_pos)

         # calculate P(negative|f)by adding the log of P(f|negative)
         try:
            n_f_neg = self.neg_dict[feature] + 1
         except: # word does not exist in dict, # of (feature and negative) = 1 (smoothing)
            n_f_neg = 1
         # print "number of " + feature + " in negative " + str(n_f_neg)
         p_f_neg = float(n_f_neg) / (n_positive+n_negative)
         # print "debug: # of feature that is negative " + str(n_f_neg) + "; # of negative " + str(n_negative)
         p_f_neg = float(p_f_neg) / p_neg
         p_neg_fs = p_neg_fs + math.log(p_f_neg)

      # compare P(positive|fs) and P(negative|fs)
      if p_pos_fs > p_neg_fs:
         result = "positive"
      elif p_pos_fs < p_neg_fs:
         result = "negative"
      else:
         result = "neutral"
      return result

   def testDataset(self):
      """Recursively test the review's sentiment in dataset folder."""
      # First, get the names of all the files in "dataset" directory
      # and stores them in fileNames
      positive = 0
      negative = 0
      neutral = 0
      num = 0
      print "Start testing on tweets---"
      fileNames = []
      for fFileObj in os.walk("dataset/"):
         fileNames = fFileObj[2]
         break
      for fname in fileNames:
         text = self.loadFile(fname,"dataset/")
         senti = self.classify(text)
         num += 1
         if senti == "positive":
            positive += 1
         elif senti == "negative":
            negative += 1
         elif senti == "neutral":
            neutral += 1
      print "Done. Here's the result:"
      print "Out of " + str(num) + " examples, \n" + str(positive) + " are positive;\n" + str(negative) + " are negative;\n" + str(neutral) + " are neutral."


   def loadFile(self, sFilename, folderName):
      """Given a file name, return the contents of the file as a string."""

      f = open(folderName+sFilename, "r")
      sTxt = f.read()
      f.close()
      return sTxt
   
   def save(self, dObj, sFilename):
      """Given an object and a file name, write the object to the file using pickle."""

      f = open(sFilename, "w")
      p = pickle.Pickler(f)
      p.dump(dObj)
      f.close()
   
   def load(self, sFilename):
      """Given a file name, load and return the object stored in the file."""

      f = open(sFilename, "r")
      u = pickle.Unpickler(f)
      dObj = u.load()
      f.close()
      return dObj

   def tokenize(self, sText): 
      """Given a string of text sText, returns a list of the individual tokens that 
      occur in that string (in order)."""

      lTokens = []
      sToken = ""
      for c in sText:
         if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-":
            sToken += c
         else:
            if sToken != "":
               lTokens.append(sToken)
               sToken = ""
            if c.strip() != "":
               lTokens.append(str(c.strip()))
               
      if sToken != "":
         lTokens.append(sToken)

      return lTokens

if __name__ == "__main__":
   bc = Bayes_Classifier()
   bc.testDataset()