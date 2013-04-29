select * from word where word_type="None";
update word set word_type="adg." where word_type="None" and translation like "adg.%";
update word set word_type="ipf." where word_type="None" and translation like "ipf.%";
update word set word_type="ipf," where word_type="None" and translation like "ipf,%";
update word set word_type="pf." where word_type="None" and translation like "pf.%";
update word set word_type="sf." where word_type="None" and translation like "sf.%";
update word set word_type="sn." where word_type="None" and translation like "sn.%";
update word set word_type="sm." where word_type="None" and translation like "sm.%";