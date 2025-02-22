# Python Crash Course 


## Project 

> Input 
```python 
class Event: 
    def __init__(self,data,user,machine,type):
        
        self.date = date
        self.user = user
        self.machine = machine
        self.type = type

def current_users(events):
  events.sort(key=get_event_date)
  machines = {}
  for event in events:
    if event.machine not in machines:
      machines[event.machine] = set()
    if event.type == "login":
      machines[event.machine].add(event.user)
    elif event.type == "logout":
      machines[event.machine].remove(event.user)
  return machines

def generate_report(machines):
  for machine, users in machines.items():
    if len(users) > 0:
      user_list = ", ".join(users)
      print("{}: {}".format(machine, user_list))
```

> Output 

List of users currently logged into machines. 

### Hints 
```python
numbers = [4,6,2,7,1]
numbers.sort() 
names = ['Johnatan', 'Jane', 'Jack',"Elizabeth", "Mary"]
sorted(numbers,key=lambda x: len(x),reverse=False)
```

