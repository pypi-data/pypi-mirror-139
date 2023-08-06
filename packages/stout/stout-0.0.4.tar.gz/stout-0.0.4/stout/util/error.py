from traceback import format_exc

def detailed_error():
    ''' returns traceback as an list of strings

            example:
                from stout.util import detailed_error

                try: create_error()
                except:
                        
                    err = detailed_error()
                    print(err)
    '''
    return format_exc().splitlines()