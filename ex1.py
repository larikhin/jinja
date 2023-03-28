from jinja2 import Template

name = "Федор"
age = 37

tm = Template('Привет {{ n.upper() }}, тебе {{ a*2 }}!')
msg = tm.render(n=name, a=age)

print(msg)


class Person():
    def __init__(self, name, age):
        self.name = name
        self.age = age


per = Person('Федя', 32)
print(per.age, per.name)
tmpl = Template('Привет {{ p.name }}, тебе {{ p.age }}!')
mesg = tmpl.render(p=per)
print(mesg)

per = {'name':'Вася', 'age':'44'}
mesg = tmpl.render(p=per)
print(mesg)

per = {'name':'Вася', 'age':'55'}
tmpl = Template("Привет {{ p['name'] }}, тебе {{ p['age'] }}!")
mesg = tmpl.render(p=per)
print(mesg)