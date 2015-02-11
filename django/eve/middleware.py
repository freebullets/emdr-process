from django.db import connection
from django.template import Template, Context
import string 
#http://djangosnippets.org/snippets/161/
class SQLLogMiddleware:
    def process_response ( self, request, response ):
        #Don't print SQL queries for binary outputs!        if istext(response.content) == 0:            return response 
        time = 0.0
        for q in connection.queries:
            time += float(q['time'])
 
        t = Template('''
            <p><em>Total query count:</em> {{ count }}<br/>
            <em>Total execution time:</em> {{ time }}</p>
            <ul class="sqllog">
                {% for sql in sqllog %}
                    <li>{{ sql.time }}: {{ sql.sql }}</li>
                {% endfor %}
            </ul>
        ''')
 
        response.content = "%s%s" % ( response.content, t.render(Context({'sqllog':connection.queries,'count':len(connection.queries),'time':time})))
        return response
 
#http://code.activestate.com/recipes/173220-test-if-a-file-or-string-is-text-or-binary/
def istext(s):
    if "" in s:
        return 0
 
    if not s:  # Empty files are considered text
        return 1
 
    # Get the non-text characters (maps a character to itself then
    # use the 'remove' option to get rid of the text characters.)
    t = s.translate(string.maketrans("", ""), "".join(map(chr, range(32, 127)) + list("nrtb"))) 
    # If more than 30% non-text characters, then
    # this is considered a binary file
    if float(len(t))/len(s) >= 0.30:        return 0