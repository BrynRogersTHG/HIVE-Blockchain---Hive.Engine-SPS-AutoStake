# HIVE-Blockchain---Hive.Engine-SPS-AutoStake

@ -0,0 +1,36 @@
Stake your SPS every few minutes, automatically.

When writing this script, I found several other script to auto-stake but they all 
were written during the time of the airdrop and contained a bunch of code that is now redundant. 

I wanted something more simple, to fire up and keep running all day. Due to the fact
I have a large SPS stake and plenty of RC's, I keep mine claiming at every 60 seconds.

The script needs a couple of modifications to work, one is your HIVE username, and the other,
your posting key.

**posting_key = '5xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
username = 'your-user-name'**

Replace the above with your own value.

**delay = 60**

Set the delay in seconds depending on how often you want to claim and compound your SPS.

I am still not convinced that the below code works, and auto-switches if there are node issues.

nodes = ['https://api.hive.blog', 'https://api.deathwing.me', 'https://anyx.io']
hive = Hive(node=nodes, keys=[posting_key])
set_shared_blockchain_instance(hive)

However, most problems go away if you simply re-try. It could be down to the first node in the list
being hammered. I still get timeouts and errors with the above so added a Try: in one of @bauloewe's routines.

Speaking of @bauloewe, I used part of his code to create mine (after speaking with him on Discord and
asking his permission). He told me his code was open-source, although I could not find these parts on his
personal GitHub repo)

Usage once the variable names have been modified is 'python SPSStake_1.2.py'

This one does something useful, a trait I intend to continue with in future projects!