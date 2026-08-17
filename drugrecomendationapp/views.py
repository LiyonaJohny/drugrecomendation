from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect,redirect
from django.db import connection
from drugrecomendationapp.forms import mform
from drugrecomendationapp.models import mmodel
import nltk 
from django.db import connection
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize, sent_tokenize 
stop_words = set(stopwords.words('english')) 
txt = "Programers  is an program with programing languages. anila was good programmer " 
from nltk.stem import PorterStemmer
import datetime
tdate=datetime.date.today()
today=tdate.strftime("%Y-%m-%d")
todaym=tdate.strftime("%m")
# Create your views here.
def index(request):
    return render(request,"index.html")

def userreg(request):
    return render(request,"userreg.html")

def companyreg(request):
    return render(request,"companyreg.html")



def userregistration(request):
    cursor=connection.cursor()
    na=request.GET['name']
    ag=request.GET['age']
    gen=request.GET['gender']
    pl=request.GET['place']
    ad=request.GET['address']
    ph=request.GET['phone']
    em=request.GET['email']
    pw=request.GET['pwd']

    sql="insert into user(uname,age,gender,place,address,phonenum,email,password) values('%s','%s','%s','%s','%s','%s','%s','%s')"%(na,ag,gen,pl,ad,ph,em,pw)
    cursor.execute(sql)
    ut='user'
    sql2="select max(uid) as id from user"
    cursor.execute(sql2)
    result=cursor.fetchall()
    for r in result:
        sql3="insert into login(uid,uname,upass,utype) values ('%s','%s','%s','%s')"%(r[0],em,pw,ut)
        cursor.execute(sql3)    

    msg="<script>alert('User Registered Successfully!');window.location='/index/';</script>"
    return HttpResponse(msg)

def companyregistration(request):
    cursor=connection.cursor()
    na=request.GET['name']
    pl=request.GET['place']
    ad=request.GET['address']
    ph=request.GET['phone']
    em=request.GET['email']
    pw=request.GET['pwd']

    sql="insert into company(cname,place,address,phonenum,email,password) values('%s','%s','%s','%s','%s','%s')"%(na,pl,ad,ph,em,pw)
    cursor.execute(sql)
    ut='company'
    sql2="select max(cid) as id from company"
    cursor.execute(sql2)
    result=cursor.fetchall()
    for r in result:
        sql3="insert into login(uid,uname,upass,utype,status) values ('%s','%s','%s','%s','false')"%(r[0],em,pw,ut)
        cursor.execute(sql3)    

    msg="<script>alert('company Registered Successfully!');window.location='/index/';</script>"
    return HttpResponse(msg)


def login(request):
    return render(request,"login.html")
def loginuser(request):
    cursor=connection.cursor()
    p=request.GET['name']
    q=request.GET['pwd']
    sql="select * from login where uname='%s' and upass='%s'"%(p,q)
    cursor.execute(sql)

    if(cursor.rowcount) > 0:
        result=cursor.fetchall()
        for row in result:
            request.session['uid']=row[1]
            request.session['uname']=row[2]
            request.session['upass']=row[3]
            request.session['utype']=row[4]
            if(request.session['utype']=='company' and row[5]=='true'):
                return render(request,'companyhome.html')

        # else:
        #     msg="<script>alert('Invalid Company');window.location='/login/';</script>"
        # return HttpResponse(msg)
        
            elif(request.session['utype']=='user'):
                return render(request,'userhome.html')

            elif(request.session['utype']=='admin'):
                return render(request,'adminhome.html')
            
            elif(request.session['utype']=='doctor'):
                return render(request,'doctorhome.html')

        
        
    else:
        msg="<script>alert('Invalid username and password');window.location='/login/';</script>"
    return HttpResponse(msg)
        
def companyhome(request):
    return render(request,"companyhome.html")
def viewcompany(request):
    cursor=connection.cursor()
    uid=request.session['uid']
    s="select * from company where cid='%s'"%(uid)
    cursor.execute(s)
    rs=cursor.fetchall()
    use=[]
    for row in rs:
        q={'cid':row[0],'cname':row[1],'place':row[2],'address':row[3],'phonenum':row[4],'email':row[5]}
        use.append(q)
    return render(request,'viewcompany.html',{'use':use})

def userhome(request):
    return render(request,'userhome.html')
def vmedicine(request):
    cursor=connection.cursor()
    
    s="select * from med_details "
    print(s)
    cursor.execute(s)
    rs=cursor.fetchall()
    tk=[]
    for row in rs:
        q={'med_id':row[0],'name':row[1],'used':row[2],'mg':row[3],'dosage':row[4],'cmp':row[5],'effects':row[6],'pres':row[7],'pack':row[8],'image':row[9]}
        tk.append(q)
    return render(request,'vmedicine.html',{'tk':tk})

def meddetail(request):
    cursor=connection.cursor()
    mid=request.GET['mid']
    s="select * from med_details where med_id='%s'"%(mid)
    print(s)
    cursor.execute(s)
    rs=cursor.fetchall()
    tk=[]
    for row in rs:
        q={'med_id':row[0],'name':row[1],'used':row[2],'mg':row[3],'dosage':row[4],'cmp':row[5],'effects':row[6],'pres':row[7],'pack':row[8],'image':row[9]}
        tk.append(q)
    s="select * from review where med_id='%s'"%(mid)
    cursor.execute(s)
    cursor.execute(s)
    rs=cursor.fetchall()
    rv=[]
    for row in rs:
        q={'rid':row[0],'uid':row[1],'med_id':row[2],'date':row[3],'review':row[4],'rating':row[5]}
        rv.append(q)

    return render(request,'meddetail.html',{'tk':tk,'rv':rv})

def companyupdation(request):
    cursor=connection.cursor()
    cpid=request.session['uid']
    s="select * from company where cid='%s'"%(cpid)
    cursor.execute(s)
    rs=cursor.fetchall()
    tk=[]
    for row in rs:
        q={'cid':row[0],'cname':row[1],'place':row[2],'address':row[3],'phonenum':row[4],'email':row[5]}
        tk.append(q)
    return render(request,'companyupdation.html',{'tk':tk})

def companyupdate(request):
    cursor=connection.cursor()
    cpid=request.session['uid']
    s="select * from company where cid='%s'"%(cpid)
    cursor.execute(s)
    rs=cursor.fetchall()
    tk=[]
    for row in rs:
        q={'cid':row[0],'cname':row[1],'place':row[2],'address':row[3],'phonenum':row[4],'email':row[5]}
        tk.append(q)
    return render(request,'companyupdation.html',{'tk':tk})
    
def companyupdation1(request):
    cursor=connection.cursor()
    id=request.GET['id']
    name=request.GET['name']
    place=request.GET['place']
    address=request.GET['address']
    phoneno=request.GET['phone']
    email=request.GET['email']
    sql="update company set cname='%s',place='%s',address='%s',phonenum='%s',email='%s' where cid='%s'" %(name,place,address,phoneno,email,id)
    cursor.execute(sql)
    msg="<script>alert('Updated Successfully!');window.location='/companyhome/';</script>"
    return HttpResponse(msg)

# def viewuser(request):
#     return render(request, 'viewuser.html')

def viewuser(request):
    cursor=connection.cursor()
    # uid=request.session['uid']
    s="select * from user "
    cursor.execute(s)
    rs=cursor.fetchall()
    use=[]
    for row in rs:
        q={'uid':row[0],'uname':row[1],'age':row[2],'gender':row[3],'place':row[4],'address':row[5],'phonenum':row[6],'email':row[7]}
        use.append(q)
    
    return render(request,'viewuser.html',{'use':use})

def userupdate(request):
    cursor=connection.cursor()
    usid=request.session['uid']
    s="select * from user where uid='%s'"%(usid)
    cursor.execute(s)
    rs=cursor.fetchall()
    tk=[]
    for row in rs:
        q={'uid':row[0],'uname':row[1],'age':row[2],'gender':row[3],'place':row[4],'address':row[5],'phonenum':row[6],'email':row[7]}
        tk.append(q)
    return render(request,'updateuser.html',{'tk':tk})

def userupdation1(request):
    cursor=connection.cursor()
    id=request.GET['id']
    name=request.GET['name']
    age=request.GET['age']
    gender=request.GET['gender']
    place=request.GET['place']
    address=request.GET['address']
    phoneno=request.GET['phone']
    email=request.GET['email']
    sql="update user set uname='%s',age='%s',gender='%s',place='%s',address='%s',phonenum='%s',email='%s' where uid='%s'" %(name,age,gender,place,address,phoneno,email,id)
    cursor.execute(sql)
    msg="<script>alert('Updated Successfully!');window.location='/userhome/';</script>"
    return HttpResponse(msg)

def adminhome(request):
    return render(request,'adminhome.html')

def adminviewcompany(request):
    cursor=connection.cursor()
    s="select * from company inner join login on login.uid=company.cid where login.utype='company'"
    cursor.execute(s)
    rs=cursor.fetchall()
    use=[]
    for row in rs:
        q={'cid':row[0],'cname':row[1],'place':row[2],'address':row[3],'phonenum':row[4],'email':row[5],'status':row[12]}
        use.append(q)
    return render(request,'adminviewcompany.html',{'use':use})

def approvecompany(request):
    cursor=connection.cursor()
    cpid=request.GET['id']
    s="update login set status='true' where uid='%s' and utype='company'"%(cpid)
    cursor.execute(s)

    msg="<script>alert('Approved Successfully!');window.location='/adminhome/';</script>"
    return HttpResponse(msg)

def rejectcompany(request):
    cursor=connection.cursor()
    cpid=request.GET['id']
    s="update login set status='false' where uid='%s' utype='company'"%(cpid)
    cursor.execute(s)

    msg="<script>alert('Approved Successfully!');window.location='/adminhome/';</script>"
    return HttpResponse(msg)

def addmedicine(request):
    return render(request,"addmedicine.html")

# def meddetails(request):
#     cursor=connection.cursor()
#     na=request.GET['name']
#     us=request.GET['used']
#     mg=request.GET['mg']
#     ds=request.GET['dosage']
#     cmp=request.GET['cmp']
#     eff=request.GET['effects']
#     pr=request.GET['pres']
#     pk=request.GET['pack']
#     img=request.GET['image']

#     sql="insert into med_details(name,used,mg,dosage,cmp,effects,pres,pack,image) values('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(na,us,mg,ds,cmp,eff,pr,pk,img)
#     cursor.execute(sql)

#     msg="<script>alert('Details added Successfully!');window.location='/companyhome/';</script>"
#     return HttpResponse(msg)

def viewmedicine(request):
    cursor=connection.cursor()
    s="select * from med_details"
    cursor.execute(s)
    rs=cursor.fetchall()
    use=[]
    for row in rs:
        q={'med_id':row[0],'name':row[1],'used':row[2],'mg':row[3],'dosage':row[4],'cmp':row[5],'effects':row[6],'pres':row[7],'pack':row[8],'image':row[9]}
        use.append(q)
    
    return render(request,"viewmedicine.html",{'use':use})

def med(request):
    if request.method=="POST":
        medforms=mform(request.POST,request.FILES)
        if medforms.is_valid ():
            meds=mmodel()
            meds.name=request.POST['name']
            meds.used=request.POST['used']
            meds.mg=request.POST['mg']
            meds.dosage=request.POST['dosage']
            meds.cmp=request.POST['cmp']
            meds.effects=request.POST['effects']
            meds.pres=request.POST['pres']
            meds.pack=request.POST['pack']
            meds.image=medforms.cleaned_data["image"]

            meds.save()
            m='medicine'
            msg="<script>alert('successfully added');window.location='/addmedicine/';</script>"
            saved=True
            return HttpResponse(msg)
    
        else:
            medforms=mform()
            # msg="<script>alert('Details added Successfully!');window.location='/addmedicine/';</script>"
        return HttpResponse(msg)
    

# def medupdate(request):
#     mid=request.GET['id']
#     return render(request,"medupdate.html" ,{"mid":mid} )

def medicineupdate(request):
    cursor=connection.cursor()
    mid=request.GET['id']
    s="select * from med_details where med_id='%s'"%(mid)
    cursor.execute(s)
    rs=cursor.fetchall()
    tk=[]
    for row in rs:
        q={'med_id':row[0],'name':row[1],'used':row[2],'mg':row[3],'dosage':row[4],'cmp':row[5],'effects':row[6],'pres':row[7],'pack':row[8]}
        tk.append(q)
    return render(request,'medicineupdate.html',{'tk':tk})

def medupdation(request):
    cursor=connection.cursor()
    mid=request.GET['id']
    name=request.GET['mname']
    used=request.GET['used']
    mg=request.GET['mg']
    dosage=request.GET['dosage']
    cmp=request.GET['cmp']
    effects=request.GET['effects']
    pres=request.GET['pres']
    pack=request.GET['pack']
    sql1="update med_details set name='%s',used='%s',mg='%s',dosage='%s',cmp='%s',effects='%s',pres='%s',pack='%s' where med_id='%s'" %(name,used,mg,dosage,cmp,effects,pres,pack,mid)
    cursor.execute(sql1)
    msg="<script>alert('Updated Successfully!');window.location='/viewmedicine/';</script>"
    return HttpResponse(msg)

# def medicine(request):
#     cursor=connection.cursor()
#     mid=request.GET['id']
#     s="select * from med_details where used='%s'"%(search)
#     cursor.execute(s)
#     rs=cursor.fetchall()
#     tk=[]
#     for row in rs:
#         q={'med_id':row[0],'name':row[1],'used':row[2],'mg':row[3],'dosage':row[4],'cmp':row[5],'effects':row[6],'pres':row[7],'pack':row[8]}
#         tk.append(q)
#     return render(request,'userhome.html',{'tk':tk})
def smedicine(request):
    cursor = connection.cursor()
    med = request.GET['med']
    print(med)

    s = f"""
        SELECT med_details.med_id,
               med_details.name,
               med_details.used,
               med_details.mg,
               med_details.dosage,
               med_details.cmp,
               med_details.effects,
               med_details.pres,
               med_details.pack,
               med_details.image,
               COALESCE(AVG(review.rating), 0) AS rate
        FROM med_details
        LEFT JOIN review ON review.med_id = med_details.med_id
        WHERE med_details.used LIKE '%{med}%'
           OR med_details.name LIKE '%{med}%'
        GROUP BY med_details.med_id
        ORDER BY rate DESC
        LIMIT 20;
    """

    print(s)
    cursor.execute(s)
    rs = cursor.fetchall()
    tk = []
    for row in rs:
        q = {
            'med_id': row[0],
            'name': row[1],
            'used': row[2],
            'mg': row[3],
            'dosage': row[4],
            'cmp': row[5],
            'effects': row[6],
            'pres': row[7],
            'pack': row[8],
            'image': row[9],
            'rating': row[10]
        }
        tk.append(q)

    return render(request, 'vmedicine.html', {'tk': tk})



def addreview(request):
    return render(request,"addreview.html")

def review(request):
    cursor = connection.cursor()
    uid = request.session["uid"]
    na = request.GET['mid']
    # dt = request.GET['date']
    re = request.GET['review']

    ##############################################
    sql2 = "truncate table postag"
    cursor.execute(sql2)
    ################post tag & stop words  ######################
    txt = request.GET["review"]
    txtstring = txt
    tokenized = sent_tokenize(txt)
    for i in tokenized:
        wordsList1 = nltk.word_tokenize(i)
        wordsList = [w for w in wordsList1 if not w in stop_words]
        tagged1 = nltk.pos_tag(wordsList)
        tagged = [(word, tag) for word, tag in tagged1 if (
            tag == 'NN' or tag == 'NNS' or tag == 'NNP' or tag == 'NNPS' or tag == 'JJ' or tag == 'JJR' or tag == 'JJS' or tag == 'VB' or tag == 'VBD' or tag == 'VBG' or tag == 'VBN' or tag == 'VBP' or tag == 'VBZ')]
        for f, g in tagged1:
            sql = "insert into postag(data) values('%s')" % (f)
            cursor.execute(sql)
    you = []
    sql3 = "select * from postag"
    cursor.execute(sql3)
    result1 = cursor.fetchall()
    for row1 in result1:
        d = row1[1]
        you.append(d)
    sentence = ' '.join(you)

    #######stemming####
    ps = PorterStemmer()
    words = word_tokenize(sentence)
    w1 = []
    w2 = ''
    sql2 = "truncate table stemming"
    cursor.execute(sql2)
    for w in words:
        sql = "insert into stemming(data) values('%s')" % (ps.stem(w))
        cursor.execute(sql)
        w1.append(ps.stem(w))
        print(w, " : ", ps.stem(w))
    w2 = ' '.join(w1)

    #############posword
    sql2 = "truncate table pword"
    cursor.execute(sql2)
    sql3 = "select * from stemming"
    cursor.execute(sql3)
    result = cursor.fetchall()
    for row in result:
        sql3 = "select * from positive"
        cursor.execute(sql3)
        result1 = cursor.fetchall()
        for row1 in result1:
            if(row[1] in row1[1]):
                sql = "insert into pword(pword) values('%s')" % (row[1])
                cursor.execute(sql)
    sqlp = "select * from pword "
    cursor.execute(sqlp)
    c1 = cursor.fetchall()
    p = []
    for r in c1:
        f = {'data': r[1]}
        p.append(f)

    ############negword

    sql2 = "truncate table nword"
    cursor.execute(sql2)
    sql3 = "select * from stemming"
    cursor.execute(sql3)
    result = cursor.fetchall()
    for row in result:
        sql3 = "select * from negative"
        cursor.execute(sql3)
        result1 = cursor.fetchall()
        for row1 in result1:
            if(row[1] == row1[1]):
                sql = "insert into nword(nword) values('%s')" % (row[1])
                cursor.execute(sql)

    sqlp = "select * from nword "
    cursor.execute(sqlp)
    c1 = cursor.fetchall()
    p = []
    for r in c1:
        f = {'data': r[1]}
        p.append(f)

    ##################score

    sqlp = "select count(*) from pword "
    cursor.execute(sqlp)
    p1 = cursor.fetchall()
    for r in p1:
        pcount = r[0]
    sqlp = "select count(*) from nword "
    cursor.execute(sqlp)
    n1 = cursor.fetchall()
    for r in n1:
        ncount = r[0]
    pscore = float(pcount) / (float(pcount) + float(ncount))
    negscore = float(ncount) / (float(pcount) + float(ncount))
    sentiscore = (float(pcount) - float(ncount)) / (float(pcount) + float(ncount))
    data = []
    s1 = "positive count=" + str(pscore) + "\n"
    s2 = "negative count=" + str(negscore) + "\n"
    s3 = "sentimental count=" + str(sentiscore) + "\n"
    w = {'data': s1}
    data.append(w)
    w1 = {'data': s2}
    data.append(w1)
    w2 = {'data': s3}
    data.append(w2)

    ###########result

    sqlp = "select count(*) from pword "
    cursor.execute(sqlp)
    p1 = cursor.fetchall()
    for r in p1:
        pcount = r[0]
    sqlp = "select count(*) from nword "
    cursor.execute(sqlp)
    n1 = cursor.fetchall()
    for r in n1:
        ncount = r[0]
    count = float(pcount) + float(ncount)
    sentiscore = (float(pcount) - float(ncount)) / (float(pcount) + float(ncount))
    avgcount = sentiscore / float(count)
    # return HttpResponse(avgcount)
    if (avgcount > 0.25):
        sentilabel = 5
        sql = "insert into review(uid,med_id,date,review,rating)values('%s','%s','%s','%s','%s')" % (
            uid, na, today, re, sentilabel)
        cursor.execute(sql)
    elif (avgcount < 0.25 and avgcount > 0.00):
        sentilabel = 4
        sql = "insert into review(uid,med_id,date,review,rating)values('%s','%s','%s','%s','%s')" % (
            uid, na, today, re, sentilabel)
        cursor.execute(sql)
    elif (avgcount == -0.25):
        sentilabel = 2
        sql = "insert into review(uid,med_id,date,review,rating)values('%s','%s','%s','%s','%s')" % (
            uid, na, today, re, sentilabel)
        cursor.execute(sql)
    elif (avgcount < 0.25):
        sentilabel = 1
        sql = "insert into review(uid,med_id,date,review,rating)values('%s','%s','%s','%s','%s')" % (
            uid, na, today, re, sentilabel)
        cursor.execute(sql)
    else:
        sentilabel = 3
        sql = "insert into review(uid,med_id,date,review,rating)values('%s','%s','%s','%s','%s')" % (
            uid, na, today, re, sentilabel)
        cursor.execute(sql)
    ###############################################

    msg = "<script>alert('Review Added');window.location='/vmedicine/';</script>"
    return HttpResponse(msg)


from datetime import datetime


def doctorreg(request):
    return render(request,"doctorreg.html")

def doctorregistration(request):
    cursor=connection.cursor()
    na=request.GET['name']
    spl=request.GET['Specilization']
    nm=request.GET['number']
    ql=request.GET['qualification']
    em=request.GET['email']
    pw=request.GET['password']

    sql="insert into doctor(name,specilization,license,qualification,email,password) values('%s','%s','%s','%s','%s','%s')"%(na,spl,nm,ql,em,pw)
    cursor.execute(sql)
    ut='doctor'
    sql2="select max(doc_id) as id from doctor"
    cursor.execute(sql2)
    result=cursor.fetchall()
    for r in result:
        sql3="insert into login(uid,uname,upass,utype,status) values ('%s','%s','%s','%s','false')"%(r[0],em,pw,ut)
        cursor.execute(sql3)
    msg="<script>alert('Doctor Registered Successfully!');window.location='/index/';</script>"
    return HttpResponse(msg) 

def adminviewdoctor(request):
    cursor=connection.cursor()
    s="select * from doctor inner join login on login.uid=doctor.doc_id where login.utype='doctor'"
    cursor.execute(s)
    rs=cursor.fetchall()
    use=[]
    for row in rs:
        q={'doc_id':row[0],'name':row[1],'specilization':row[2],'number':row[3],'qualification':row[4],'email':row[5],'status':row[12]}
        use.append(q)
    return render(request,'adminviewdoctor.html',{'use':use})

def approvedoctor(request):
    cursor=connection.cursor()
    doc_id=request.GET['id']
    s="update login set status='true' where uid='%s' and utype='doctor'"%(doc_id)
    cursor.execute(s)

    msg="<script>alert('Approved Successfully!');window.location='/adminhome/';</script>"
    return HttpResponse(msg)

def rejectdoctor(request):
    cursor=connection.cursor()
    doc_id=request.GET['id']
    s="update login set status='false' where uid='%s' utype='company'"%(doc_id)
    cursor.execute(s)

    msg="<script>alert('Rejected!');window.location='/adminhome/';</script>"
    return HttpResponse(msg)

def doctorhome(request):
    return render(request,"doctorhome.html")

def viewdoctor(request):
    cursor=connection.cursor()
    doc_id=request.session['uid']
    s="select * from doctor where doc_id='%s'"%(doc_id)
    cursor.execute(s)
    rs=cursor.fetchall()
    use=[]
    for row in rs:
        q={'doc_id':row[0],'name':row[1],'specilization':row[2],'number':row[3],'qualification':row[4],'email':row[5]}
        use.append(q)
    return render(request,'viewdoctor.html',{'use':use})

def doctorupdation(request):
    cursor=connection.cursor()
    doc_id=request.session['uid']
    s="select * from doctor where doc_id='%s'"%(doc_id)
    cursor.execute(s)
    rs=cursor.fetchall()
    use=[]
    for row in rs:
        q={'doc_id':row[0],'name':row[1],'specilization':row[2],'number':row[3],'qualification':row[4],'email':row[5]}
        use.append(q)
    return render(request,'doctorupdation.html',{'use':use})

def doctorupdate(request):
    cursor=connection.cursor()
    id=request.GET['id']
    na=request.GET['name']
    spl=request.GET['specilization']
    nm=request.GET['number']
    ql=request.GET['qualification']
    em=request.GET['email']
    sql="update doctor set name='%s',specilization='%s',license='%s',qualification='%s',email='%s' where doc_id='%s'" %(na,spl,nm,ql,em,id)
    cursor.execute(sql)
    msg="<script>alert('Updated Successfully!');window.location='/viewdoctor/';</script>"
    return HttpResponse(msg)

def doctorlist(request):
    cursor=connection.cursor()
    s="select * from doctor"
    cursor.execute(s)
    rs=cursor.fetchall()
    use=[]
    for row in rs:
        q={'doc_id':row[0],'name':row[1],'specilization':row[2],'number':row[3],'qualification':row[4],'email':row[5]}
        use.append(q)
    return render(request,'doctorlist.html',{'use':use})


def chat(request):
    cursor=connection.cursor()
    lid=request.GET['lid']
    uid=request.session['uid']
    cd=today
    s="select * from chatm  inner join chats on chatm.chatid=chats.chatid where chatm.lid='%s' and chatm.uid='%s'"%(lid,uid)
    cursor.execute(s)
    rs=cursor.fetchall()
    alist=[]
    for r in rs:
        x={'chatid':r[0],'chatdate':r[3],'msg':r[5],'typ':r[6]}
        alist.append(x)
    return render(request,'chat.html',{'lid':lid,'uid':uid,'alist':alist})

def chataction(request):
    cursor=connection.cursor()
    uid=request.session['uid']
    lid=request.GET['lid']
    # print(lid)
    msg=request.GET['msg']
    ss="select * from chatm where uid= '%s' and lid='%s' and chatdate='%s'"%(uid,lid,today)
    cursor.execute(ss)
    if(cursor.rowcount>0):
        ss="select max(chatid) as chatid from chatm"
        cursor.execute(ss)
        rss=cursor.fetchall()
        for row in rss:
            chid=row[0]
            sql="insert into chats(chatid,msg,typ)values('%s','%s','user')"%(chid,msg)
            cursor.execute(sql)
    else:
        sql1="insert into chatm(uid,lid,chatdate) values('%s','%s','%s')"%(uid,lid,today)
        cursor.execute(sql1)
        sql2="select max(chatid) as chatid from chatm"
        cursor.execute(sql2)
        output=cursor.fetchall()
        for row in output:
            sql1="insert into chats(chatid,msg,typ)values('%s','%s','user')"%(row[0],msg)
            cursor.execute(sql1)
    msg="<script>;window.location='/chat?lid="+lid+"';</script>"
    return HttpResponse(msg)

def userlist(request):
    cursor=connection.cursor()
    lid=request.session['uid']
    # uid=request.GET['lid']
    s="SELECT * FROM user where uid in(select uid from chatm where lid= '%s')"%(lid)
    print(s)
    cursor.execute(s)
    rs=cursor.fetchall()
    use=[]
    for row in rs:
        q={'uid':row[0],'uname':row[1],'age':row[2],'gender':row[3]}
        use.append(q)
    return render(request,'userlist.html',{'use':use})

def dchat(request):
    cursor=connection.cursor()
    lid=request.session['uid']
    uid=request.GET['uid']
    
    cd=today
    s="select * from chatm  inner join chats on chatm.chatid=chats.chatid where chatm.lid='%s' and chatm.uid='%s' order by chatdate asc"%(lid,uid)
    cursor.execute(s)
    rs=cursor.fetchall()
    alist=[]
    for r in rs:
        x={'chatid':r[0],'chatdate':r[3],'msg':r[5],'typ':r[6]}
        alist.append(x)
    return render(request,'dchat.html',{'uid':uid,'lid':lid,'alist':alist})

def dchataction(request):
    cursor=connection.cursor()
    lid=request.session['uid']
    uid=request.GET['uid']
    msg=request.GET['msg']
    ss="select * from chatm where uid='%s' and lid='%s' and chatdate='%s'"%(uid,lid,today)
    cursor.execute(ss)
    if(cursor.rowcount>0):
        ss="select max(chatid) as chatid from chatm"
        cursor.execute(ss)
        rss=cursor.fetchall()
        for row in rss:
            chid=row[0]
            sql="insert into chats(chatid,msg,typ)values('%s','%s','doctor')"%(chid,msg)
            cursor.execute(sql)
    else:
        sql1="insert into chatm(lid,uid,chatdate) values('%s','%s','%s')"%(lid,uid,today)
        cursor.execute(sql1)
        sql2="SELECT max(chatid) as chatid from chatm"
        cursor.execute(sql2)
        output=cursor.fetchall()
        for row in output:
            sql1="insert into chats(chatid,msg,typ)values('%s','%s','doctor')"%(row[0],msg)
            cursor.execute(sql1)
    msg="<script>;window.location='/dchat?uid="+uid+"';</script>"
    return HttpResponse(msg)
    

from datetime import date   # ✅ Add this import

def givefeedback(request):
    if request.method == "POST":
        cursor = connection.cursor()
        uid = request.session['uid']  # logged-in user id
        feedback = request.POST['feedback']
        today = date.today()   # now works ✅

        sql = "INSERT INTO feedback(uid, feedback, fdate) VALUES ('%s','%s','%s')" % (uid, feedback, today)
        cursor.execute(sql)
        return HttpResponse("<script>alert('Feedback submitted successfully');window.location='/viewfeedback/';</script>")
    
    return render(request, "givefeedback.html")



# View all feedbacks (of that user or all users)
def viewfeedback(request):
    cursor = connection.cursor()
    uid = request.session['uid']
    sql = "SELECT fid, feedback, fdate FROM feedback WHERE uid='%s'" % (uid)
    cursor.execute(sql)
    rs = cursor.fetchall()
    fb = []
    for row in rs:
        q = {'fid': row[0], 'feedback': row[1], 'fdate': row[2]}
        fb.append(q)
    return render(request, "viewfeedback.html", {"fb": fb})


def admin_viewfeedback(request):
    cursor = connection.cursor()
    sql = """
        SELECT f.fid, u.uname, f.feedback, f.fdate
        FROM feedback f 
        JOIN user u ON f.uid = u.uid
        ORDER BY f.fdate DESC
    """
    cursor.execute(sql)
    rs = cursor.fetchall()
    fb = []
    for row in rs:
        q = {
            'fid': row[0],
            'uname': row[1],
            'feedback': row[2],
            'fdate': row[3]
        }
        fb.append(q)
    return render(request, "admin_viewfeedback.html", {"fb": fb})
