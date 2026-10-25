######HS26_SoCo-group_03-a2#########
Order in which part 1 was coded:

1. Arithmetics and comparison operations. These where quite straightforward

2. if statements. A bit trickier. Needed to add a few lines in the do() function... this might not be the best practice. 

3. started coding one dimentional arrays. Noticed it might be easier to do so after allowing the user to declare types. Will leave this for later in the project.

4. None and print. 

5. Type anotations. Started modifying do_func before noticing it is do_call() that breaks with type annotation. Undid the previous work and moved the extentions/modifications to do_call().

6. Struct definition. Added a global TYPES dictionary to store user-defined types.

7. make() to instanciate a struct.

8. field_get, field_set.

9. new_array. 

TO DO NEXT:
10. finish implementing arrays. 
11. Tasks 2 and 3

NOTES FOR PAUL:
there might be something to tackle with arrays and do(). Do() dispatches as long as what we are feeding it is a list... but if we have our array type it might confuse things (maybe not, but we should watch out). 



