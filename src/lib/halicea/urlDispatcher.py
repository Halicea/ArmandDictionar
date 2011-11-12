from django.template import Template
matchMap =(
    ("TestTemplate","cms/{{controller}}/{{action}}",
     "Kosta", {"controller":'Base', "action":"Index"}
    )
)
templates= []
for k in matchMap:
    templates.append({k[0]:(Template(k[1],k[0]), k[2], k[3])})

def reverse_url(controller, params):
    
    return ("Kosta", {"controller":"kosta", "action":"zdravo"})
def test():
    controller, params = reverse_url("/cms/kosta/zdravo")
    print controller, params

test()
    
        