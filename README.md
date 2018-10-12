jc2cli
======

This is JC-to-CLI, it is just another command line interface framework making
use of python prompt_toolkit module.

jc2cli takes all code from obsolete jc2li package, and revamp the way commands
are being handled and created.

It basically keeps working with decorators, but behavior is moved from the
decorator and a full tree is created for handling it.

Branch v.1.0.prompt.2.0 makes use of prompt-toolkit 2.0 and legacy syntax handling, 
where mostly all logic is embedded in decorators.
