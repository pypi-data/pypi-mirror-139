def error(msg):
    return f"\n<error>{'ERRER'+' ':>12}</error>{msg}\n"

def status(status,msg):
    return f"<status>{status+' ':>12}</status>{msg}"

def sccuess(status,msg):
    return f"<sccuess>{status+' ':>12}</sccuess>{msg}"
