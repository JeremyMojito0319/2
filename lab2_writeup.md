# lab2_writeup

My main work include the following points:

- Features implemented (drafts): Generate Note (modal + /api/notes/generate), Translate (title + content via /api/notes/<id>/translate), drag-drop reorder (frontend + POST /api/notes/reorder).
- LLM integration: src/llm.py contains call_llm_model, translate_to_language, extract_structured_notes. Added warnings.filterwarnings to suppress Trio runtime warning.
- Security: token.txt removed from git tracking; .env in .gitignore. Recommend revoking exposed PAT.
- Deployment plan: Frontend to Vercel (static), Backend to Render/Railway or container, Database moved to Supabase (Postgres). Use vercel.json rewrites to proxy /api to backend.

Above all, when adding the function, screenshots of each adjustment step were not taken. Therefore, the following images are based on the chat records with Copilot.

## A. Features implemented 

### 1. Record date, time and tags

After lab1, I added the new function of "Record date, time and tags", and adjusted the page layout according to the interface design.

![image-20251018190835749](C:\Users\16799\AppData\Roaming\Typora\typora-user-images\image-20251018190835749.png)

### 2. drag feature:

I added the drag-and-drop new function using AI, and also added the front-end and back-end at the same time. However, the first deployment of the function was unsuccessful. I asked the AI to redo it and the result was satisfactory.![image-20251018190512310](C:\Users\16799\AppData\Roaming\Typora\typora-user-images\image-20251018190512310.png)

#### 3.Translate feature:

Then, I used AI to add a new translation function for me.I introduced the llm.py file and deployed the sample code, instructing the AI to perform the translation function.When adding the translate function, I found that to enable the AI, not only the front-end needs to be modified but also a database must be added, along with the corresponding backend. Otherwise, there will only be the corresponding translate button but the function cannot be realized.

![image-20251018190150317](C:\Users\16799\AppData\Roaming\Typora\typora-user-images\image-20251018190150317.png)

![image-20251018191156064](C:\Users\16799\AppData\Roaming\Typora\typora-user-images\image-20251018191156064.png)

### 4.Generate Note

In the "generate note" section, the design of the front-end interface was generally not satisfactory. The "generate note" button was always placed within the "add note" section. Through communication with the AI and adjustments, the desired effect was finally achieved.

![image-20251018191500583](C:\Users\16799\AppData\Roaming\Typora\typora-user-images\image-20251018191500583.png)

### 5. Fix bug

Time adding bug I found that if no time is added in the "add note" section, and then the note is generated, the default time for that note is set as "today". 

This would be a problem, and it will misguide the reader.

![image-20251018191917287](C:\Users\16799\AppData\Roaming\Typora\typora-user-images\image-20251018191917287.png)

![image-20251018192341886](C:\Users\16799\AppData\Roaming\Typora\typora-user-images\image-20251018192341886.png)

It hasn't been properly modified. After that, I ask AI fix that bug again 

![image-20251018192825598](C:\Users\16799\AppData\Roaming\Typora\typora-user-images\image-20251018192825598.png)

Finally it works.

## B. Security

In the previous submission, I accidentally uploaded the token to the repository. Later, I took measures to remedy the situation to prevent any security issues.

![image-20251018193221163](C:\Users\16799\AppData\Roaming\Typora\typora-user-images\image-20251018193221163.png)

## C. Deploying my notetaking app to Vercel

I then deployed my completed project to Vercel. I also wrote a plan for converting the database using GPT-5 mini.

![image-20251018194817047](C:\Users\16799\AppData\Roaming\Typora\typora-user-images\image-20251018194817047.png)

After I registered the Supabase project and copy the project URL to the .env. I used Copilot to convert SQLite to Supabase (PostgreSQL)

![image-20251019121500767](C:\Users\16799\AppData\Roaming\Typora\typora-user-images\image-20251019121500767.png)

Test the connection

![image-20251019122053392](C:\Users\16799\AppData\Roaming\Typora\typora-user-images\image-20251019122053392.png)

After running the Python test program, it was found that the connection to the Supabase database could not be established. Later, it was discovered that the method for the Supabase connection settings needed to be set to "session pooler", and then the connection was successful.

![image-20251019124943851](C:\Users\16799\AppData\Roaming\Typora\typora-user-images\image-20251019124943851.png)

When I deployed to Vercel, I found that since the initial files I downloaded were in the project folder, I didn't have the permission to change the file status. I could only keep it as private. So, I created a new repository on my own GitHub and uploaded my project to this public repository. In this way, Vercel could add this public project.

![image-20251019142918480](C:\Users\16799\AppData\Roaming\Typora\typora-user-images\image-20251019142918480.png)Previously, I mistakenly submitted the file "token.txt". I will delete the submission record.

![image-20251019144046652](C:\Users\16799\AppData\Roaming\Typora\typora-user-images\image-20251019144046652.png)

Later, I found that it was difficult to clear the records in the terminal. So I deleted the git records, submitted all the contents to a new repository and deployed it to Vercel.After the re-deployment was successful, there was still a persistent error message. Then I view the Vercel deployment log 

![image-20251019150657487](C:\Users\16799\AppData\Roaming\Typora\typora-user-images\image-20251019150657487.png)

I used the following in src/llm.py: 
token = os.environ["GITHUB_TOKEN"]
However, this environment variable was not set on Vercel, causing Python to fail to find it and thus throwing an exception directly.

![image-20251019154138051](C:\Users\16799\AppData\Roaming\Typora\typora-user-images\image-20251019154138051.png)

During the re-deployment process, it is necessary to add the corresponding environment variables in Vercel. Initially, I used the default database URL. However, I found that the log error message was attempting to use IPv6. Therefore, I forced the use of the IPv4 connection of the pooler in Supabase. After re-deploying in the Vercel environment variables, I found that the log error did not indicate a failure in database connection, which indicates that the connection has been successfully established.

![image-20251019154242137](C:\Users\16799\AppData\Roaming\Typora\typora-user-images\image-20251019154242137.png)

Finally deployed successfully with copilot

![image-20251019202744958](C:\Users\16799\AppData\Roaming\Typora\typora-user-images\image-20251019202744958.png)

![image-20251019202800753](C:\Users\16799\AppData\Roaming\Typora\typora-user-images\image-20251019202800753.png)