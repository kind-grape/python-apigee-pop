# common var modules to define varibles that are used in modules
# would need to define the private key and public key. This example is reading those from files
objPrivate = open("/Users/richp/Desktop/hvac_test/new_pop/pop-private-key-pkcs8.pem","r")
objPublic  = open("/Users/richp/Desktop/hvac_test/new_pop/pop-public-key.pem","r")
strPrivate = objPrivate.read()
strPublic  = objPublic.read()