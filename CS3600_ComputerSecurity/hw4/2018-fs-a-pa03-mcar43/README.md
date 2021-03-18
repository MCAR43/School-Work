# Programming assignment 3 (pa03) -- Practical end-to-end user cryptography

1. Create ssh key and set it up to log into gitlab/git-classes, take screenshots of it functioning.
Read the following links in full:
    * https://git-classes.mst.edu/help/ssh/README#generating-a-new-ssh-key-pair
    * https://www.digitalocean.com/community/tutorials/understanding-the-ssh-encryption-and-connection-process
    * https://help.github.com/articles/connecting-to-github-with-ssh/ (and sub-pages)

2. Fully validate the Kali iso your downloaded for pa00, from within Kali.
Take screenshots of hash and signature verification steps.
    * https://docs.kali.org/introduction/download-official-kali-linux-images
    * https://www.kali.org/downloads/

3. Set up email encryption using gnupg.

    1. Read the content at all of the links here: 
    http://web.mst.edu/~taylorpat/Index_files/PublicKey.html

    2. Create a gpg2 key with 4096 bit RSA and your campus email. 
    
    3. Set up your email a in mail client (optional), see the following for supported clients: https://en.wikipedia.org/wiki/GNU_Privacy_Guard#Application_support.
    or use webmail with https://www.mailvelope.com/en/
    
    4. Exchange keys with 5 students in 3600 (either in person, or using a keyserver like https://keys.mailvelope.com/ with any client you choose).
    
    5. Encrypt separate back-and-forth discussions with 5 different students in 3600;
    take a single screenshot for each back-and-forth exchange.
    
    6. Get those same 5 students to sign your gpg2 public key at the command line in Kali;
    include your signed key in your repo, and optionally (above) on the mailvelope keyserver.
    
    7. Send a single signed message encrypted to both me and and our TA/grader (Jeff Gould <jg7f9@mst.edu>) with your 5x-peer-signed and ASCII-armored public key attached to the email.
    The subjet line should exactly read: "3600 pa03 gnupg email"

4. With 5 students in the class (can be different or the same as for previous part), exchange back-and-forth communications in an open-source end-to-end PFS app of your choosing.
    
    1. Read: https://en.wikipedia.org/wiki/Forward_secrecy and https://en.wikipedia.org/wiki/Deniable_authentication first, then choose an app:
        * https://wire.com/
        * https://tox.chat/
        * https://ring.cx/
        * https://www.signal.org/
        * https://silence.im/
        * OTR (many clients on Jabber/XMPP, IRC, etc) or OMEMO. Both are open federated protocol with multiple applications
            * https://en.wikipedia.org/wiki/Off-the-Record_Messaging
            * https://en.wikipedia.org/wiki/OMEMO
            * https://conversations.im/
            * https://gajim.org/
            * https://chatsecure.org/
        * Retroshare signed messenging capabilities http://retroshare.net/
        * https://ricochet.im/
        * http://goldbug.sourceforge.net/
    
        If you are aware of any others, please feel free to check with me to see if they meet the criteria.
    
    2. Include screenshots in the repository of 5 exchanges. 
