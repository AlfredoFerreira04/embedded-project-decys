# Introduction

This is the second part of the embedded assignment. Start from Part 1 before proceeding to this second part.

# PART 2: Final Boss

## Identify Cryptographic Assets
Joe says some of the cryptographic data extracted is familiar, but he can't pinpoint why that is so.
Maybe look at the strings or entropy of the firmware and reveal suspicious information.

**TARGET 4: Identify the cryptographic data**
>Hint:
>Some data may stand out due to how it is encoded.
>After decoding, it is usually trivial to infer if we are dealing with an encrypted block, or structured information via the existing magic numbers.

**Required artifact (under `TARGETS/target-4/`).** The extracted key and signature (base64), an entropy scan of the firmware, and the first lines of `openssl asn1parse` / `openssl rsa -text` on your key.

**Answer this (from *your* board).** What is the key size, which structural (ASN.1/DER) bytes told you what it was, how many bytes is the encrypted signature, and how does the key region's entropy compare to a code region?



## Find the pot of gold
After some `openssl` back and forth, it seems we were able to extract a hash of some kind from the signature. Fortunately, we have a very comprehensive (and short...) rainbow table we can use to reveal the hashed intel.

**TARGET 5: c&c password**

**Required artifact (under `TARGETS/target-5/`).** The decrypted `hash` file, your `openssl` decrypt transcript, and the rainbow-table lookup result.

**Answer this (from *your* board).** What is the MD5 hash recovered from your decrypted signature, what is the recovered c&c password, and why is a *short* rainbow table enough here?



## Crack the code
The messages we found hint at a random number generator and our reverse engineering team found a bug that leads to the code repeating after some attempts. But it seems the codes are different on each boot...

**TARGET 6: Crack the OTP generator**

**Required artifact (under `TARGETS/target-6/`).** A raw serial capture of your OTP attempts showing the repeat, the recovered generator parameters, and a reproduction of the next expected value. This should be a `.txt` file.

**Answer this (from *your* board).** On this boot, how many attempts until the generator repeated, what value repeated, and what is the next OTP the generator will produce?



## Connect to the C&C
With the C&C password in our hands, and with the OTP system cracked, we can finally connect to their servers!

**TARGET 7: Final secret**

**Required artifact (under `TARGETS/target-7/`).** The full serial transcript of the successful C&C connection, showing OTP acceptance and the final-secret line.

**Answer this (from *your* board).** How did targets 5 and 6 combine to let you connect?

