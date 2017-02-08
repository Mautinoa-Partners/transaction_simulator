def greet_me(**kwargs):
    if kwargs is not None:
        for key, value in kwargs.iteritems():
            print "%s == %s" %(key,value)

if __name__ == '__main__':

    args = {'parliament':'gloryhallastoopid', 'funkadelic':'cosmic slop'}
    greet_me(**args)
