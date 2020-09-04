from html.parser import HTMLParser

import htmlmin

from github import Github

import github

import pandas as pd

df = pd.read_excel("HTML_Assignment_Scores_RDIP2.0.xlsx")

#print(df.columns)

g = Github("6853f416ab003f27ec4efdaf51ee1aceb9cc6fa5")

start_tags, end_tags, attributes = [], [], []

class Parser(HTMLParser):
  
  def handle_starttag(self, tag, attrs):

    global start_tags, attributes

    start_tags.append(tag)

    for attr in attrs:

        attributes.append(attr)
   
  def handle_endtag(self, tag):
    
    global end_tags
    
    end_tags.append(tag)

parser = Parser()

def marks_allocation(path, inputfile):

    start_tags.clear(), end_tags.clear(), attributes.clear()

    score, count, count1, count_list, count_attr, count_r, count_c = 0, 0, 0, 0, 0, 0, 0

    parser.feed(htmlmin.minify(inputfile))

    #print(list(set(end_tags)))

    if path == 'details.html':
        #print(list(set(end_tags)))

        for tag in list(set(start_tags)):

            if tag == 'img':

                score += 1

        for tag in list(set(end_tags)):

            if tag == 'html':

                count += 1

            if tag == 'a':

                score += 1

            if len(tag) == 2 and tag.lower().startswith("h") and count1 == 0:

                score += 1

            if tag == 'body':

                count += 1

            if tag == 'title':

                count += 1

            if tag == 'ul':

                count_list += 1

            if tag == 'li':

                count_list += 1

        if count == 3:

            score += 1

        if count_list == 2:

            score += 1

    elif path == 'homepage.html':

        #print(list(end_tags))

        for tag in list(set(start_tags)):

            if tag == 'img':

                score += 1

        for tag in list(set(end_tags)):

            if tag == 'html':

                count += 1

            if tag == 'body':

                count += 1

            if tag == 'title':

                count += 1

            if tag == 'ul':

                count_list += 1

            if tag == 'li':

                count_list += 1

            if tag == 'a':

                score += 1

            if tag == 'p':

                score += 1

            if tag == 'table':

                score += 1

            if tag == 'tr':

                score += 1

            if tag == 'td':

                score += 1

            if tag == 'th':

                score += 1

            if len(tag) == 2 and tag.lower().startswith("h") and count1 == 0:

                score += 1

                count1 += 1

        if count == 3:

            score += 1

        if count_list == 2:

            score += 1

    elif path == 'registration.html': 

        for tag in list(set(start_tags)):

            if tag == 'img':

                score += 1

        for tag in list(set(end_tags)):

            if tag == 'html':

                count += 1

            if tag == 'body':

                count += 1

            if tag == 'title':

                count += 1

            if tag == 'ul':

                count_list += 1

            if tag == 'li':

                count_list += 1

            if tag == 'a':

                score += 1

                #print("IMG3")

            if tag == 'p':

                score += 1

            if tag == 'form':

                score += 1
                #print("IMG4")

            if tag == 'table':

                score += 1
                #print("IMG5")

            if tag == 'tr':

                score += 1

            if tag == 'td':

                score += 1

            if tag == 'th':

                score += 1

            if len(tag) == 2 and tag.lower().startswith("h") and count1 == 0:

                score += 1

                count1 += 1
                #print("IMG6")
        if count == 3:

            score += 1
            #print("IMG1")

        if count_list == 2:

            score += 1

        for attr in attributes:
            
            if attr[0] == 'type' and attr[1] == 'submit':

                score += 1
                #print("IMG16")

            if attr[0] == 'action':

                score += 1
                #print("IMG7")

            if attr[0] == 'method':

                score += 1
                #print("IMG8")

            if attr[0] == 'type' and attr[1] == 'text' and count_attr == 0:

                score += 1

                count_attr += 1
                #print(count_attr)
                #print("IMG9")

            if attr[0] == 'type' and attr[1] == 'email':

                score += 1
                #print("IMG10")

            if attr[0] == 'type' and attr[1] == 'radio' and count_r <= 3:

                score += 1

                count_r += 1
                #print("IMG13")

            if attr[0] == 'type' and attr[1] == 'checkbox' and count_c <= 4:

                score += 0.5

                count_c += 1
               # print("IMG15")

            if attr[0] == 'type' and attr[1] == 'reset':

                score += 1
              #  print("IMG17")

    else:

        score = 0
 
    return score

def final_scores():

    final_scores_dict = {}

    flag = False

    unitid, submissionid, studentid, finalscore, comment = [], [], [], [], []

    handle = []

    for commiturl in df['tasksubmission']:

        handle.append(commiturl.split('https://github.com/')[1].split('/')[0])

        df['tasksubmission'] = df['tasksubmission'].replace(commiturl, commiturl.split('https://github.com/')[1].split('/')[0])

    files = ['Details.html', 'Registration.html', 'Homepage.html']

    for handles in handle:

        studentid.append(df.loc[df['tasksubmission'] == handles]['studentId'].values[0])

        submissionid.append(df.loc[df['tasksubmission'] == handles]['submissionId'].values[0])

        unitid.append(1)

        final_score, flag, exception = 0, False, False

        try:

            x = g.get_user(handles)

        except github.GithubException as e:

            comment.append("Wrong Github Handle Provided")

            finalscore.append(0)

            continue

        for repo in x.get_repos():

            if repo.name.lower() == 'rdip':
                
                flag = True

                try:

                    repo.get_contents("")

                except github.GithubException as e:

                    exception = True

                    #comment.append("Empty Repository")

                    #finalscore.append(0)

                    continue

                for i in repo.get_contents(""):

                    if i.path in files:

                        score = marks_allocation(i.path, i.decoded_content.decode("utf-8"))

                        final_score += score

                break

        if final_score == 0 and flag == True and exception == False:

            comment.append("Wrong Files Submitted")

        elif final_score == 0 and flag == False and exception == False:

            comment.append("rdip repository not found")

        elif final_score == 0 and flag == True and exception == True:

            comment.append("Empty Repository")

        else:

            comment.append("Valid")

        finalscore.append(final_score)

    final_scores_dict['UnitId'] = unitid
    final_scores_dict['SubmissionId'] = submissionid
    final_scores_dict['Studentid'] = studentid
    final_scores_dict['Final_Score'] = finalscore
    final_scores_dict['Comments'] = comment
    #print(final_scores_dict)
    fd = pd.DataFrame.from_dict(final_scores_dict)
    fd.to_excel("output.xlsx")
    #print(fd)
final_scores()