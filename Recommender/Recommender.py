#Cheng Yijun   TA: Nicholas Farrow   Assignment 10
class Recommender:
	def __init__(self, books_filename,rating_filename):
		self.books_filename=books_filename
		self.rating_filename=rating_filename
		self.dict1={}

	def read_books(self,file_name):
		value=[]
		i=0
		c=[]
		try:
			f=open(file_name,'r')
		except:
			return None
		for line in f:
			value=line.split(',')
			a=value[1]
			b=a.strip()
			c.append(b)
			c.append(value[0])
			self.dict1[i]=c
			i=i+1
			c=[]
		return self.dict1
		
	def read_users(self,user_file):
		value2=[]
		i=[]
		dict2={}
		try:
			fr=open(user_file,'r')
		except:
			return None
		for lines in fr:
			value2=lines.split()
			j=value2[0]
			for integer in value2[1:]:
				i.append(int(integer))
			dict2[j]=i
			i=[]
		return dict2


	def calculate_average_rating(self):
		avgdict={}
		dict2=self.read_users('ratings.txt')
		tot=[]
		i=[]
		count=0
		count2=0
		num=[]
		n=0
		ii=0
		for key in dict2:
			count=count+1
			i=dict2[key]
			for pp in i:
				n=n+1
				nn=n
			n=0	
		for index in range(nn):
			tot.append(0.00)
			num.append(0)
			
		for key in dict2:
			i=dict2[key]
			for pf in i:
				if pf ==0:
					count2+=1
				else:
					tot[count2]=tot[count2]+pf
					num[count2]=num[count2]+1
					count2=count2+1
				
			count2=0
	
		for tt in tot:
			if num[count2]==0:
				print 'no rating for this book'
			else:
				av=tt/num[count2]
				avgdict[ii]=round(av,2)
				ii=ii+1
				count2+=1
		return avgdict

			
	def lookup_average_rating(self,index):
		strr=self.dict1[index]
		avgdict=self.calculate_average_rating()
		avg=str(avgdict[index])
		rtbook='('+avg+')'+' '+strr[0]+'by'+strr[1]
		rtbook=rtbook.strip()
		return rtbook

	def calc_similarity(self,user1,user2):
		similarity=0
		dict2=self.read_users('ratings.txt')
		a=dict2[user1]
		b=dict2[user2]
		for n in  range(len(a)):
			similarity=(a[n]*b[n])+similarity
		return similarity
		
	def get_most_similar_user(self, current_user_id):
		maxs=0
		dict2=self.read_users('ratings.txt')
		b=dict2[current_user_id]
		similarity=0
		for key in dict2:
			if key !=current_user_id:
				a=dict2[key]
				for n in range(len(a)):
					similarity=(a[n]*b[n])+similarity
			if similarity>maxs:
				maxs=similarity
				userid=key
			similarity=0
		return userid
		
	def recommend_books(self, current_user_id):
		avgdict=self.calculate_average_rating()
		su=self.get_most_similar_user(current_user_id)
		dict2=self.read_users('ratings.txt')
		a=dict2[current_user_id]
		b=dict2[su]
		recolist=[]
		for h in range(len(a)):
			if  (a[h]==0):
				if (b[h]==3)or(b[h]==5):
					rtbok=self.lookup_average_rating(h)
					recobok=rtbok
					recolist.append(recobok)
		return recolist
				

def main():
	RC=Recommender('books.txt','ratings.txt')
	RC.read_books('books.txt')		
	print RC.dict1

	dict2=RC.read_users('ratings.txt')
	print dict2['Ben']
	avgdict=RC.calculate_average_rating()
	print avgdict
	index=input('please enter the book index:')
	rtbook=RC.lookup_average_rating(index)
	print rtbook
	a=raw_input('user1:')
	b=raw_input('user2:')
	simila=RC.calc_similarity(a,b)
	print simila
	
	c=raw_input('current user:')
	userid=RC.get_most_similar_user(c)
	print userid
	
	recolist=RC.recommend_books(c)
	print recolist
	
			
	
if __name__=='__main__':
	main()




