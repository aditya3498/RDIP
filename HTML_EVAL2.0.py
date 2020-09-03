from html.parser import HTMLParser

import htmlmin

from github import Github

import github

import pandas as pd

df = pd.read_excel("HTML_Assignment_Scores_RDIP2.0.xlsx")

#print(df.columns)

g = Github("d81914d796c3d80cfbe26ef421b2bb80b67c2e9a")

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

    score, count, count1, count_list, count_attr = 0, 0, 0, 0, 0

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

            if attr[0] == 'type' and attr[1] == 'radio':

                score += 1
                #print("IMG13")

            if attr[0] == 'type' and attr[1] == 'checkbox':

                score += 0.5
               # print("IMG15")

            if attr[0] == 'type' and attr[1] == 'reset':

                score += 1
              #  print("IMG17")

    else:

        score = 0
 
    return score

def final_scores():

    final_scores_dict, handle_studentid = {}, {}

    flag = False

    final_scores_dict["Scores"] = {}

    handle = []

    for commiturl in df['tasksubmission']:

        handle.append(commiturl.split('https://github.com/')[1].split('/')[0])

        df['tasksubmission'] = df['tasksubmission'].replace(commiturl, commiturl.split('https://github.com/')[1].split('/')[0])

    files = ['details.html', 'registration.html', 'homepage.html']

    for handles in handle:

        final_scores_dict['UnitId'] = 1

        final_scores_dict['studentId'] = df.loc[df['tasksubmission'] == handles]['submissionId'].values[0]

        final_scores_dict['submissionId'] = df.loc[df['tasksubmission'] == handles]['studentId'].values[0]

        final_score, flag = 0, False

        try:

            x = g.get_user(handles)

        except github.GithubException as e:

            final_scores_dict["Comments"] = "Wrong Github Handle Provided"

            final_scores_dict['Scores']['details.html'] = 0

            final_scores_dict['Scores']['homepage.html'] = 0

            final_scores_dict['Scores']['registration.html'] = 0

            final_scores_dict['FinalScore'] = 0

        for repo in x.get_repos():

            if repo.name == 'rdip':
                
                flag = True

                try:

                    f = repo.get_contents("")

                except github.GithubException as e:

                    final_scores_dict['Comments'] = "Repository Empty"

                    final_scores_dict['Scores']['details.html'] = 0

                    final_scores_dict['Scores']['homepage.html'] = 0

                    final_scores_dict['Scores']['registration.html'] = 0

                    final_scores_dict['FinalScore'] = 0

                    continue
                #print(f)

                for i in f:

                    if i.path in files:

                        score = marks_allocation(i.path, i.decoded_content.decode("utf-8"))

                        print(score)

                        final_scores_dict['Scores'][i.path] = score

                        final_score += score

                break

        if final_score == 0 and flag == True:
            #print(repo.name + handles)

            final_scores_dict['Comments'] = "Wrong Files Submitted"

            final_scores_dict['Scores']['details.html'] = 0

            final_scores_dict['Scores']['homepage.html'] = 0

            final_scores_dict['Scores']['registration.html'] = 0

        elif final_score == 0 and flag == False:

            final_scores_dict["Comments"] = "rdip repository not found"

            final_scores_dict['Scores']['details.html'] = 0

            final_scores_dict['Scores']['homepage.html'] = 0

            final_scores_dict['Scores']['registration.html'] = 0

        else:

            final_scores_dict['Comments'] = "VALID"

        final_scores_dict['FinalScore'] = final_score

        print(final_scores_dict)

final_scores()