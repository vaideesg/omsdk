Foundation Principles
=====================

The foundation principles are the principles that must be followed at all the times.  The principles are:
1. Dell EMC Principle
2. OA-AO Principle
3. Ease of Use Principle
4. Repeatable Principle
5. Consistency Principle
6. SPORTS Principle

# Dell EMC Principle
APIs must always be consistent with Dell EMC Systems Management Strategy and Best Practices of the relevant Product lines.

# OA-AO (One API for An Operation) Principle
An Operation is a task, job or action that results in a desired end state of the system.
1. Do not create multiple APIs for the same operation.
2. Do not combine two independent tasks into an API (for example, do not combine Server Configuration and Operating System Deployment into one API)
3. For operations taking long time, the API must allow for both synchronous and asynchronous options.
    1.  In synchronous case, the API will wait till the operation completes
    2.  In case of asynchronous case, the API will return immediately with an handle. The user can poll for status using that handle.
    3.  A variant of asynchronous option is to allow the user to specify a callback.
    4.  Have an timeout variable.  The API must exit when that timeout occurs. Timeout should be the maximum time that the API will wait altogether in that API (including all loops, waits, retries and internal timeouts). This definition brings confidence to API users that the API will not take more than a fixed time.
    5.  When a timeout occurs, return failure from the API.
4. Keep all the APIs modular
5. APIs must be transparent to protocol and other internals. Remember, the customer wants to do something with your system. Protocols just provide you a way to achieve that operation. Just because the system supports multiple protocols, it does not mean you should expose that to user.  While you hide it, you can also create a preferences which allows users to specify their own protocol choice if they want. Design should always assume that users first choice is to do it Dell's way.

# Ease of Use Principle
1. APIs should be easy to use.
2. APIs must hide complexity and tribal knowledge.  Example: Liason Share and Update Share simplify configuration and update use cases

# Repeatability Principle
Repeatablility means the ability to call the same API multiple times, resulting in the same end state of the system.
1. All APIs that treat multiple entities (users, NICs, Virtual Drives) when called twice should not create duplicate instances.
2. An API called twice should not result in different state of the system.  For example, calling "Clear Config" any number of times should result in the same behavior: the configuration is cleared

# Consistency Principle
Consistency is the conformity to standard principles all the time.
1. APIs must be consistent in naming - function names, API arguments, enumerations etc.
2. APIs belonging to similar function must be consistent in return values - 
3. APIs must be consistent with CRUD and ACID principles.
4. APIs must cover well-rounded use cases.  Don't just add a Create API.  Instead add a Create, Modify, Delete and List APIs.  If an API is irrelevant, simply make it as not_implemented.
5. APIs must use consistent arguments for the APIs.  For example, if parameters are passed as individual arguments to Create function, they should be passed as individual arguments to list, modify and delete functions. On the other hand, if you pass a structure, you should pass a structure to all.

# SPORTS Principle
SPORTS is an acronym for Simple, Portable, Optimal, Reliable, Transparent and Scalable
1. APIs must be simple. APIs must hide complexity and tribal knowledge from the consumer.
2. APIs must be transparent to the platform on which it is executed. Avoid C/C++/Native or Platform dependent code.  Example: If you have plan to write a python wrapper on a C-based tool, how would you support custom Linux installations? Your C-based tool need to be also supported for those Linux Installations as well - which is a bigger burden. Instead go with pure-python implementation. In that case, as long as python community supports the python in that custom installation, we are good. 
3. API implementations must be written optimally.  Don't write voluminous code which can be written in fewer lines
3. APIs must use only reliable dependencies - stable and supported dependent components
4. APIs must be transparent to the protocol being used
5. APIs must be thread-safe and scalable
6. APIs should not allow user to specify parameters if it does not make sense.


