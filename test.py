from functions import save_to_database, delete_from_database, generate_element_id, create_database, create_task

db = 'data'

create_database(db)

element_id = generate_element_id(db,'NT')
element = 'Testing DAY'
date = '21/10/2023'
deadline = None
field1 = ''
field2 = ''
field3 = ''
project = ''
delegated = ''
cooperating = ''
field4 = ''
field5 = ''
remarks = ''
keywords = ''
category = 'task'
done = 'No'

save_to_database(db, element_id, element, date, deadline, field1, field2, field3, project, delegated, 
                         cooperating, field4, field5, remarks, keywords, category, done)

#element_id = 'NT69_21/10/2023'
#delete_from_database(db, element_id)