from marshmallow import Schema, fields, post_load, ValidationError, validates, validate

class Person():
    def __init__(self, name, age, email):
        self.name=name
        self.age=age
        self.email=email
        
    def __repr__(self):
        return f"{self.name} is {self.age} years old."


class PersonSchema(Schema):
    name=fields.Str(validate=validate.Length(max=5))
    age=fields.Int()
    email=fields.Email() # Marshmallow by default does not check that we have these attr in input data
    location=fields.Str(required=False)
    
    @validates("age")
    def validate_age(self, age):
        if age>100 or age<20:
            raise ValidationError("Does not match age criteria.")
    
    @post_load
    def create_person(self, data, **kwargs):
        return Person(**data)
    
input_data={"name":"John", "age": 10, "email":"john@gmail.com"}

try:
    schema=PersonSchema()
    person=schema.load(input_data) # validation is performed only on load/deserialization (not on serialization)
    
    #print(person)
    
    result=schema.dump(person) 
    print(result)
except ValidationError as err:
    print(err)
    print(err.valid_data) # allows us to see what data WAS valid
    

        