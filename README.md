# How to use this
Here is Bob and Alice
```
('40e6215d-b5c6-4896-987c-f30f3678f608','Alice',300),
('6ecd8c99-4036-403d-bf84-cf8400f67836','Bob',1000)
```


POST this json on __localhost:5000/__
```
{
	"sender": "40e6815d-b5c6-4896-987c-f30f3678f608",
	"receiver": "6ecd8c99-4036-403d-bf84-cf8400f67836",
	"amount": 1
}
```
You should get
```
{
  "message": "Done successfully"
}
```
You can go to __localhost:8080/__  
__System:__ postgres  
__Server:__ db  
__Username:__ example  
__Password:__ example  
__Database:__ example  
To look into __DB__ and see whats changin'  

Also you can modify first json whatever you like and still get an informative answer  

Or just run `python3 -m pytest -sv` after deployment and watch for the output  