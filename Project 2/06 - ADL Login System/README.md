# ADL Login System

![img](ADLLoginSystem.JPG)

This is a login page, telling us to input a username and a password.

When seeing this, I thought of SQL injection.

The most simple SQL injection is:

	' or 1=1 -- 
	**Note: There's a space in the back**

So we input this in the username section and login....

![img2](ADLLoginSystem-SOL.JPG)

If no space behind the `--` then both the username and password section need to input the same thing

![img3](ADLLoginSystem-SOL1.JPG)
	
Yet there is another solution:

	' or 1=1 #
	
![img4](ADLLoginSystem-SOL2.JPG)

These SQL injection works because they make the rest part of the SQL code into comments.


Normal SQL code to obtain and check username and password:

	SELECT * FROM users WHERE name = '$name' and password = '$password'

Hence with `'` at the beginning of our input, and the comment symbol at the end of our input, the code becomes:

	SELECT * FROM users WHERE name = '' or '1'='1' -- and password = '$password'
	SELECT * FROM users WHERE name = '' or '1'='1' #and password = '$password'
	
Therefore, it only checks the username input, which is `'' or '1'='1'`, and will undoubtedly return 1. 

(Everything, on the same line, after `-- ` and `#` is turned into comments)

	

	
