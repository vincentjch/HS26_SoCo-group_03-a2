###### HS26_SoCo-group_03-a2 #########
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

10. Debugging print. Passed the whole args into do() method instead of the argument so every print crashed before.

11. new_array gets only type and length because name comes from the set.

12. Struct annotations were crashing in do_call, TYPES["Point"] is a field list and not a standard python type. I added helpers py with is_of_type().

13. range, for, array_get, array_set. extensions.mth runs completely with that, but sq_sum still showed 0. Arrays just remain python lists, which works fine with do().

Order in which part 2 was coded:

1. argparse for filename, --max-depth, --debug. SETTINGS dict to store them, like TYPES.

2. --max-depth needed type=int, values from the command line stayed strings

3. notnull and notzero modifiers in do_call. 

4. Recursion limit with a depth counter in do_call. Also array_size, annotations.mth needs it.

5. --debug needed action="store_true", the first fix was wrong

Order in which part 3 was coded:

1. do_debug with c, g and q. Mixed up c and g at first and then fixed it later.

2. counter in debug.mth stayed 0, same problem as sq_sum. env_set now updates the variable where it already exists.

Final fixes for part 1, after going through the assignment again:

1. mod only forbids 0 now, instead of 0 and <0.

2. Comparisons return 1 or 0 instead of True/False.

3. new_array read the type from args[1], so float arrays got 0 instead of 0.0. Struct arrays are filled with 0, kept it simple.

4. Struct name check outside the loop, keywords like func are not allowed.

5. make and field_set use is_of_type, field_set gives an error for unknown fields.

6. Return types are checked in do_call.

AI usage: see AI_usage.md.

