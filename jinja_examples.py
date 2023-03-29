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

# Без кранирования
data = '''
Jinja вместо определения {{ name }}
подставляет соответствующее определение'''
tm = Template(data)
msg = tm.render(name='Feodor')
print(msg)

# С экранированием {% raw %}  {% endraw %}
data = '''
{% raw %}Jinja вместо определения {{ name }}
подставляет соответствующее определение{% endraw %}'''
tm = Template(data)
msg = tm.render(name='Feodor')
print(msg)

# экранирование спецсимволов {{ link | e}} e-escape , render(link=link)
link = '''
В HTML документе ссылки определяются так: 
<a href="#">ссылка</a>'''
tm_without_e = Template(link)
msg_without_e = tm_without_e.render()
tm = Template("{{link | e}}")
msg = tm.render(link=link)
print(msg_without_e, msg)

from markupsafe import escape
link = '''
В HTML документе ссылки определяются так: 
<a href="#">ссылка</a>'''
msg = escape(link)
print(msg)

# выражение for
cities = [{'id': 1, 'city': 'Moscow'},
          {'id': 2, 'city': 'SPb'},
          {'id': 3, 'city': 'Kazan'},
          {'id': 4, 'city': 'Pushkin'},
          {'id': 5, 'city': 'Kirovsk'}, ]
link = '''
<select name="cities">
{%- for c in cs -%}
    <option value={{c['city']}}>{{c['city']}}</option>
{% endfor -%}
</select>
'''
tm = Template(link)
msg = tm.render(cs=cities)
print(msg)


# выражение if
cities = [{'id': 1, 'city': 'Moscow'},
          {'id': 2, 'city': 'SPb'},
          {'id': 3, 'city': 'Kazan'},
          {'id': 4, 'city': 'Pushkin'},
          {'id': 5, 'city': 'Kirovsk'}, ]
link = '''
<select name="cities">
{%- for c in cs -%}
{% if c.id>2 -%}
    <option value={{c['city']}}>{{c['city']}}</option>
{% elif c.city=='SPb'-%}
    <option value={{c['city']}}>elif is activated {{c['city']}}</option>
{% else -%}
    <option value={{c['city']}}>else is activated {{c['city']}}</option>
{% endif -%}
{% endfor -%}
</select>
'''
tm = Template(link)
msg = tm.render(cs=cities)
print(msg)

# определение sum() sum(iterable, attribute=None, start=0)
cars = [{'model': 'Audi', 'price': 43_000},
        {'model': 'Sckoda', 'price': 33_000},
        {'model': 'Ford', 'price': 17_000},
        {'model': 'VAZ', 'price': 23_000},
        {'model': 'Tesla', 'price': 63_0_00}, ]
# снаружи двойные, внутри одинарные кавычки!
tpl = '''
cars is: {{ cs }}
Total price for cars: {{ cs | sum( attribute = 'price' ) }}
'''
tm = Template(tpl)
msg = tm.render(cs=cars)
print(msg)

digs = [1,2,3,4,5,6,7]
tpl = ' the sum is: {{digs | sum}}'
tm = Template(tpl)
msg = tm.render(digs=digs)
print(msg)

'''
List of Builtin Filters
https://jinja.palletsprojects.com/en/2.11.x/templates/#template-inheritance
'''
# снаружи двойные, внутри одинарные кавычки!
tpl = '''
cars is: {{ cs }}
Max price for cars, dict: {{ cs | max( attribute = 'price' ) }}
the model is {{ (cs | max( attribute = 'price' )).model }}
the price is {{ (cs | max( attribute = 'price' )).price }}

Min price for cars, dict: {{ cs | min( attribute = 'price' ) }}
the model is {{ (cs | min( attribute = 'price' )).model }}
the price is {{ (cs | min( attribute = 'price' )).price }}

Random price for cars: {{ (cs | random()).price }}

Replace letters for dict: {{ cs | replace("e","E") }}
'''
tm = Template(tpl)
msg = tm.render(cs=cars)
print(msg)

persons = [{'name': 'Alexey'},
           {'name': 'Ivan'},
           {'name': 'Petr'},]
tpl = '''
{% for w in usersss -%}
{% filter upper%} {{w.name}} {% endfilter %}
{% endfor -%}'''
print(Template(tpl).render(usersss = persons))

# macro определения DRY
html = '''
{% macro input_name_tmpl(name, value='', type='text', size=20) -%}
 <input type="{{type}}" name={{name}} value="{{value|e}}" size={{size}}>
{%- endmacro %}
<p>{{ input_name_tmpl('username') }}
<p>{{ input_name_tmpl('email') }}
<p>{{ input_name_tmpl('password') }}
'''
tm = Template(html)
msg = tm.render()
print(msg)

html = '''
{% macro list_users(list_of_user) -%}
    <ul>{% for i in list_of_user %}
        <li>{{i.name}}
    {%- endfor %}
    </ul>
{% endmacro %}
{{list_users(users)}}
'''
print(Template(html).render(users = persons))

html = '''
{% macro list_users(list_of_user) -%}
    <ul>{% for i in list_of_user %}
        <li>{{caller(i)}}
    {%- endfor %}
    </ul>
{% endmacro %}

{% call(i) list_users(users) %}
<ul>
<li>{{i}}
<li>{{i.name}}
<li>{{i.name}}
</ul>
{% endcall %}
'''
print(Template(html).render(users = persons))

#Вызов шаблона из файла
from jinja2 import Environment, FileSystemLoader

persons = [{'name': 'Alexey', 'old': 18, 'weight': 76},
           {'name': 'Ivan', 'old': 34, 'weight': 90},
           {'name': 'Petr', 'old': 23, 'weight': 86},
           {'name': 'Vasya', 'old': 33, 'weight': 68}, ]

file_loader = FileSystemLoader('folder_name')
env = Environment(loader=file_loader)
tm = env.get_template('main.html')
msg = tm.render(users=persons)
print(msg)

#Вызов функции
from jinja2 import Environment, FunctionLoader


def loadTpl(path):
    if path == 'index':
        return '''Имя {{users.name}}, {{users.old}}'''
    else:
        return '''Данные: {{u}}'''

func_loader = FunctionLoader(loadTpl)
env = Environment(loader=func_loader)
tm = env.get_template('index')
msg = tm.render(users=persons[0])
print('\n')
print(msg)


#Наследование страниц
from jinja2 import Environment, FileSystemLoader


file_loader = FileSystemLoader('folder_name')
env = Environment(loader=file_loader)
tm = env.get_template('page.html')
msg = tm.render(title="Заголовок страницы", footer_info='Инфо для футера')
print(msg)

# Дополнение шаблонов страниц

file_loader = FileSystemLoader('folder_name')
env = Environment(loader=file_loader)
tm = env.get_template('about.html')
msg = tm.render(list_tables=persons)
print(msg)
