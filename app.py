import psycopg2
from sqlalchemy import create_engine, ForeignKey, Column,String,Integer,CHAR
from sqlalchemy.orm import sessionmaker,declarative_base
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__) 

Base= declarative_base()

#create Table
class Person(Base):
    __tablename__="person"
    
    ssn=Column("ssn", Integer, primary_key=True)
    name=Column("name", String)
    gender=Column("gender", CHAR)
    age=Column("age", Integer )
    
    def __init__(self,ssn,name,gender,age):
        self.ssn=ssn
        self.name=name
        self.gender=gender
        self.age=age
    
    def __repr__(self):
        return f"({self.ssn} {self.name} {self.gender} {self.age})"


def db_connect():
    db_url = 'postgresql://postgres:1111@localhost:5432/postgres'

    engine=create_engine(db_url)
    Base.metadata.create_all(bind=engine)
    Session=sessionmaker(bind=engine)
    session=Session()
    return session

##HOME
@app.route('/') 
def index(): 
    # Connect to the database 
    session=db_connect()

    # Fetch the data 
    data=session.query(Person).order_by(Person.ssn.asc()).all()#session.query(Person).all()
    #print(data)
    return render_template('main.html', data=data)

##ADD
@app.route('/add', methods=['POST'])
def add_person():
    # Connect to the database 
    session=db_connect()
    data=session.query(Person).order_by(Person.ssn.asc()).all()#session.query(Person).all()
   
    ssn = request.form['ssn'] 
    name = request.form['name'] 
    gender = request.form['gender'] 
    age = request.form['age']
    
    existing_person = session.query(Person).filter_by(ssn=ssn).first()
    session.close()

    if existing_person is not None:
        return render_template('main.html', data=data,msg="Person Exists")
    
    
    person=Person(ssn,name,gender,age)
    session.add(person)
    session.commit()
    
    data=session.query(Person).order_by(Person.ssn.asc()).all()
    return render_template('main.html', data=data,msg="Person Added")


##DELETE
@app.route('/delete',methods=['POST'])
def del_person():
    session=db_connect()
    data=session.query(Person).order_by(Person.ssn.asc()).all()
    ssn = request.form['ssn']
    
    existing_person = session.query(Person).filter_by(ssn=ssn).first()
    session.close()

    if existing_person is None:
        return render_template('main.html', data=data,msg1="Person Doesnt Exists")
    #delete_query
    person = session.query(Person).filter_by(ssn=ssn).first()
    session.delete(person)
    
    session.commit()
    data=session.query(Person).order_by(Person.ssn.asc()).all()
    return render_template('main.html', data=data,msg1="Deleted")



##UPDATE
@app.route('/update',methods=['POST'])
def up_person():
    session=db_connect()
    ssn = request.form['ssn'] 
    name = request.form['name'] 
    gender = request.form['gender'] 
    age = request.form['age']
    data=session.query(Person).order_by(Person.ssn.asc()).all()
    existing_person = session.query(Person).filter_by(ssn=ssn).first()
    session.close()

    if existing_person is None:
        return render_template('main.html', data=data,msg2="Person Doesnt Exists")
 
   
    
    results= session.query(Person).filter(Person.ssn==ssn).first()
    results.ssn=ssn
    results.name = name
    results.gender=gender
    results.age=age
    
    session.commit()
    data=session.query(Person).order_by(Person.ssn.asc()).all()
    return render_template('main.html', data=data,msg2="Person Updated")
    
        
if __name__ == '__main__': 
    app.run(debug=True)




