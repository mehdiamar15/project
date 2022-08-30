import os ,time
from django.shortcuts import render
from django.http import HttpResponse,Http404,JsonResponse
from .models import Board
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Board, Topic, Post
from .forms import NewTopicForm,PostForm,InputRecordsForm,Input_pmtaconfig_Form
from django.core import serializers
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView
from django.utils import timezone
from django.utils.decorators import method_decorator
import requests,webbrowser
import xml.etree.ElementTree as ET
from django.contrib import messages
import xmltodict,json
from boards.classes.namecheap import Namecheap
from boards.classes.ssh_connect import SSH_Connect
from tld import get_tld
import uuid 
import redis
namecheapclass =Namecheap()
ssh_connect=SSH_Connect()

@login_required
def pmta_config_ajax(request): 
    output_rerros=False
    
    if request.method =="POST":
        action = request.POST.get('action')
        cmnds_action = request.POST.get('cmnds')
        print(action)
        form=Input_pmtaconfig_Form(request.POST)
        output = {"success":False, "error":"", "error_form":False,  "result":"","data":""}
        isps={"1":"gmail","2":"hotmail"}
        if form.is_valid():
            
            server = form.cleaned_data.get('server')
   
            print(server)
            auth_connect =ssh_connect.auth(host=server,passwd='mH19-@yau.a')
            if auth_connect:
               
                output["success"]=True
                isp_id = form.cleaned_data.get('isp')
                print("okaaaaaaaaaaaaaaaaaay")
                output["result"]="server connected "
                print(isps[isp_id])
                if action == 'get_config':
                    getfile=ssh_connect.exec_(cmd="cat /home/gmuser_Amehdi/"+isps[isp_id]+".txt",exectimeout=10)
                    if getfile:
                        print("yes exec")
                        print(ssh_connect.output_)
                        output_pmta_g=ssh_connect.output_.decode()
                    
                        output["data"]=output_pmta_g
                        output["success"]=True
                        output["result"]='Config Pmta of  :'+isps[isp_id]+''
                    
                    
                    elif not getfile:
                        print("not okaaaaaaaaaaaaaaaaaay")
                        print(ssh_connect.error)
                        output["success"]=False
                        output["error"]=ssh_connect.error
                        output["result"]="Unfortunately , cant get config  check if the config exist in the server"
                if action == 'save_config':
                    print("save_configsave_config save_config save_config save_config save_config")
                    config_p = form.cleaned_data.get('config_p')
                   
                    print(config_p)

                    idd=uuid.uuid1()
                    fileelocal ='/var/tmp/'+str(idd)+'.txt'
                    write_in_local =ssh_connect.write_file_in_local(fileelocal,config_p)
                    if write_in_local:

                        remotefile="/home/gmuser_Amehdi/"+isps[isp_id]+".txt"
                        puting= ssh_connect.put(fileelocal, remotefile)
                        if puting:
                            output["success"]=True                          
                            output["result"]="Config has Been Changed"
                            output["data"]=config_p
                            os.system('rm -rf /var/tmp/'+str(idd)+'.txt')
                            print(idd)
                        else:
                            output["success"]=False
                            output["error"]=ssh_connect.error
                            output["result"]="Issue when put file in remote server"


                        
                        
                        if puting:
                            print("treue treuetreuetreuetreuetreuetreuetreue")
                        else:
                            print("falsefalsefl")
                    else:
                        output["success"]=False
                        output["error"]="Issue when create a file in local"
                        output["result"]="Issue when create a file in local"
                if action == 'pmta_cmnds':
                    print(cmnds_action)
                    if cmnds_action =='delete':
                        time.sleep(5)
                        print("pmta_cmndssss")
                        runcmnd=ssh_connect.exec_(cmd="/sbin/pmta delete --queue=*/*",exectimeout=10)
                        print(runcmnd)
                        if runcmnd:
                            print("!!!!!!!!!!!!!!!!!!!!!!!!!",ssh_connect.error)
                            print("???????????",ssh_connect.output_)
                            output["success"]=True
                            output["error"]=ssh_connect.output_.decode()
                            output["result"]="'Delete Action': "+ ssh_connect.output_.decode()
                        else:
                            print("!!!!!!!!!!!no!!!!!!!!!!!!!!",ssh_connect.error)
                            print("??????no?????",ssh_connect.output_)
                            output["success"]=False
                            output["error"]=ssh_connect.output_.decode()
                            output["result"]=ssh_connect.output_.decode()
                    if cmnds_action == 'pause/resume':
                        time.sleep(5)
                        print("pmta_cmndssss")
                        runcmnd=ssh_connect.exec_(cmd="/sbin/pmta pause queue */*;/sbin/pmta resume queue */*",exectimeout=10)
                        print(runcmnd)
                        if runcmnd:
                            print("!!!!!!!!!!!!!!!!!!!!!!!!!",ssh_connect.error)
                            print("???????????",ssh_connect.output_)
                            output["success"]=True
                            output["error"]=ssh_connect.output_.decode()
                            output["result"]="'Pause/Resume' Action: "+ ssh_connect.output_.decode()
                        else:
                            print("!!!!!!!!!!!no!!!!!!!!!!!!!!",ssh_connect.error)
                            print("??????no?????",ssh_connect.output_)
                            output["success"]=False
                            output["error"]=ssh_connect.output_.decode()
                            output["result"]=ssh_connect.output_.decode()
                    if cmnds_action == 'pause':
                        time.sleep(5)
                        print("pmta_cmndssss")
                        runcmnd=ssh_connect.exec_(cmd="/sbin/pmta pause queue */*",exectimeout=10)
                        print(runcmnd)
                        if runcmnd:
                            print("!!!!!!!!!!!!!!!!!!!!!!!!!",ssh_connect.error)
                            print("???????????",ssh_connect.output_)
                            output["success"]=True
                            output["error"]=ssh_connect.output_.decode()
                            output["result"]="'Pause Action': "+ ssh_connect.output_.decode()
                        else:
                            print("!!!!!!!!!!!no!!!!!!!!!!!!!!",ssh_connect.error)
                            print("??????no?????",ssh_connect.output_)
                            output["success"]=False
                            output["error"]=ssh_connect.output_.decode()
                            output["result"]=ssh_connect.output_.decode()
                    if cmnds_action == 'resume':
                        time.sleep(5)
                        print("pmta_cmndssss")
                        runcmnd=ssh_connect.exec_(cmd="/sbin/pmta resume queue */*",exectimeout=10)
                        print(runcmnd)
                        if runcmnd:
                            print("!!!!!!!!!!!!!!!!!!!!!!!!!",ssh_connect.error)
                            print("???????????",ssh_connect.output_)
                            output["success"]=True
                            output["error"]=ssh_connect.output_.decode()
                            output["result"]="'Resume Action': "+ ssh_connect.output_.decode()
                        else:
                            print("!!!!!!!!!!!no!!!!!!!!!!!!!!",ssh_connect.error)
                            print("??????no?????",ssh_connect.output_)
                            output["success"]=False
                            output["error"]=ssh_connect.output_.decode()
                            output["result"]=ssh_connect.output_.decode()

                    if cmnds_action == 'schedule':
                        time.sleep(5)
                        print("pmta_cmndssss")
                        "cat /home/gmuser_Amehdi/"+isps[isp_id]+".txt"
                        runcmnd=ssh_connect.exec_(cmd="/sbin/pmta schedule "+isps[isp_id]+".com/*",exectimeout=10)
                        print(runcmnd)
                        if runcmnd:
                            print("!!!!!!!!!!!!!!!!!!!!!!!!!",ssh_connect.error)
                            print("???????????",ssh_connect.output_)
                            output["success"]=True
                            output["error"]=ssh_connect.output_.decode()
                            output["result"]="'schedule Action': "+ ssh_connect.output_.decode()
                        else:
                            print("!!!!!!!!!!!no!!!!!!!!!!!!!!",ssh_connect.error)
                            print("??????no?????",ssh_connect.output_)
                            output["success"]=False
                            output["error"]=ssh_connect.output_.decode()
                            output["result"]=ssh_connect.output_.decode()


                    



            elif not auth_connect:
                print("not okaaaaaaaaaaaaaaaaaay")
                print(ssh_connect.error)
                output["success"]=False
                output["error"]=ssh_connect.error
                output["result"]="Unfortunately , can't connect to the server "
                print(output)

            if request.is_ajax():
                return JsonResponse(output, safe=False)
            

        else:
          
            output = {"success":False, "error":"","error_form":True,"result":"form invalid","data":form.errors.as_json()}
            return JsonResponse(output, safe=False) 

    else:
        form=Input_pmtaconfig_Form()        
    return render(request, 'pmta_config.html', {'form':form})

############################################


@login_required
def home(request):


    board_topics = Board.objects.all()
    
    count_lines =0
    if request.method =="POST":
        reque =True
        deleted = False
        added = False
        form = InputRecordsForm(request.POST)
        if form.is_valid():
            print("form.is_valid():form.is_valid():form.is_valid():form.is_valid():form.is_valid():form.is_valid():form.is_valid():form.is_valid():form.is_valid():form.is_valid():form.is_valid():form.is_valid():form.is_valid():form.is_valid():form.is_valid():form.is_valid():form.is_valid():form.is_valid():form.is_valid():form.is_valid():form.is_valid():form.is_valid():form.is_valid():form.is_valid():form.is_valid():form.is_valid():form.is_valid():")

            text_area_value = form.cleaned_data.get('emails')
            type_value = form.cleaned_data.get('type_record')

            
            for line in text_area_value.splitlines():
                spli = line.split('|')
                res = get_tld(spli[0], as_object=True,fix_protocol=True)
                print(" test subdomain     !",res.subdomain)
                print(" test domain     !",res.domain)
                print(" test tld     !",res.tld)
                print(" test fld     !",res.fld)
                
                check_domain =namecheapclass.checkdomain(res.fld)
                if check_domain:
                    if 'new_records' in request.POST:
                        namecheapclass.addrecords(res.fld,res.domain,res.tld,res.subdomain,spli[1],type_value)
                        result = namecheapclass.addrecords(res.fld,res.domain,res.tld,res.subdomain,spli[1],type_value)
                        print(result)
                        if result["success"] == True:
                            messages.success(request, res.fld+' '+' '+type_value+ ' '+result["result"])
                            count_lines =count_lines+1
                            added = True
                        
                        else:
                            messages.error(request, res.fld+' '+result["error"])
                    elif 'deleter_records' in request.POST:
                        result = namecheapclass.deleterecords(res.fld,res.domain,res.tld,res.subdomain,spli[1],type_value)
                        print(result)
                        if result["success"] == True:
                            messages.success(request, res.fld+' '+' '+type_value+ ' '+result["result"])
                            count_lines =count_lines+1
                            deleted = True
                        else:
                            messages.error(request, res.fld+' '+' '+type_value+ ' '+result["result"])

                        print("deleter_recordsdeleter_recordsdeleter_recordsdeleter_recordsdeleter_recordsdeleter_recordsdeleter_records")

                
                    
                    


                
                else:
                    messages.error(request, spli[0]+':  Domain not found')
    
        if deleted:
            messages.success(request, str(count_lines)+':  Records Deleted')

        elif added:
            messages.success(request, str(count_lines)+':  Records added')

        

        
      
                    

    
    else:
        
        print("noo")
        form = InputRecordsForm()
    list_boards = list(board_topics)
    context = {
        'boards': list_boards
    }
    
    #board_topics = Board.objects.all().values("name", "description")
    
    #boa = serializers.serialize("json", list_boards)
  

    if request.is_ajax():
        data = {'rendered_table': render_to_string('table_contents.html', context=context)}
        
        return JsonResponse(data)
      
    return render(request, 'home.html', {'boards': board_topics,'form':form})
    #return JsonResponse( {'board_topics': list_boards}, safe=False)




@login_required
def recordsmng(request):
    
    count_lines =0
    if request.method =="POST":
        action = request.POST.get('action')
        print("test mehdi test mehdi test mehdi test mehdi test mehdi test mehdi test mehditest mehdi ")
        reque =True
        deleted = False
        added = False
        form = InputRecordsForm(request.POST)
        if form.is_valid():
            

            text_area_value = form.cleaned_data.get('records')
            type_value = form.cleaned_data.get('type_record')
            ttl = form.cleaned_data.get('TTL')
            
              

            
            for line in text_area_value.splitlines():
                spli = line.split('|')
                res = get_tld(spli[0], as_object=True,fix_protocol=True)
                print(" test subdomain     !",res.subdomain)
                print(" test domain     !",res.domain)
                print(" test tld     !",res.tld)
                print(" test fld     !",res.fld)
                
                check_domain =namecheapclass.checkdomain(res.fld)
                if check_domain:
                    if 'new_records' in request.POST:
                        print("new_recordsnew_recordsnew_recordsnew_recordsnew_recordsnew_recordsnew_recordsnew_recordsnew_recordsnew_records")
                        namecheapclass.addrecords(res.fld,res.domain,res.tld,res.subdomain,spli[1],type_value,ttl)
                        result = namecheapclass.addrecords(res.fld,res.domain,res.tld,res.subdomain,spli[1],type_value,ttl)
                        print(result)
                        if result["success"] == True:
                            messages.success(request, res.fld+' '+' '+type_value+ ' '+result["result"])
                            count_lines =count_lines+1
                            added = True
                        
                        else:
                            messages.error(request, res.fld+' '+result["error"])
                    elif 'deleter_records' in request.POST:
                        result = namecheapclass.deleterecords(res.fld,res.domain,res.tld,res.subdomain,spli[1],type_value)
                        print(result)
                        if result["success"] == True:
                            messages.success(request, res.fld+' '+' '+type_value+ ' '+result["result"])
                            count_lines =count_lines+1
                            deleted = True
                        else:
                            messages.error(request, res.fld+' '+' '+type_value+ ' '+result["result"])

                        print("deleter_recordsdeleter_recordsdeleter_recordsdeleter_recordsdeleter_recordsdeleter_recordsdeleter_records")

                else:
                    messages.error(request, spli[0]+':  Domain not found')


        if deleted:
            messages.success(request, str(count_lines)+':  Records Deleted')

        elif added:
            messages.success(request, str(count_lines)+':  Records added')

    else:   
        print("noo one noo one")
        form = InputRecordsForm()
      
    return render(request, 'records.html', {'form':form})



@login_required
def recordsmng_ajax(request):
    action = request.POST.get('action')
    count_lines =0
    output = {"success":False, "error":"",  "result":"","data":""}
    if request.is_ajax() and request.method == "POST":
        
        print("test mehdi test mehdi test mehdi test mehdi test mehdi test mehdi test mehditest mehdi ")
        reque =True
        deleted = False
        added = False
        form = InputRecordsForm(request.POST)
        print(form.errors.as_json())
        print(type(form.errors.as_json()))
        output_rerros = {"success":False, "error":"",  "result":"","data":""}
        #output_rerros= form.errors.as_json()
        if form.is_valid():
            text_area_value = form.cleaned_data.get('records')
            type_value = form.cleaned_data.get('type_record')
            ttl = form.cleaned_data.get('TTL')
            
            for line in text_area_value.splitlines():
                spli = line.split('|')
               
                try:
                    res = get_tld(spli[0], as_object=True,fix_protocol=True)
                    print("res is okaaaaaaaaaaaaay res res ")
                    print(" test subdomain     !",res.subdomain)
                    print(" test domain     !",res.domain)
                    print(" test tld     !",res.tld)
                    print(" test fld     !",res.fld) 
                    check_domain =namecheapclass.checkdomain(res.fld)
                    if check_domain:
                        if action == 'new_records':
                            print("new_recordsnew_recordsnew_recordsnew_recordsnew_recordsnew_recordsnew_recordsnew_recordsnew_recordsnew_records")
                            namecheapclass.addrecords(res.fld,res.domain,res.tld,res.subdomain,spli[1],type_value,ttl)
                            result = namecheapclass.addrecords(res.fld,res.domain,res.tld,res.subdomain,spli[1],type_value,ttl)
                            print(result)
                            if result["success"] == True:
                                messages.success(request, res.fld+' '+' '+type_value+ ' '+result["result"])
                                count_lines =count_lines+1
                                added = True
                        
                            else:
                                messages.error(request, res.fld+' '+result["error"])
                        elif action == 'deleter_records':
                            result = namecheapclass.deleterecords(res.fld,res.domain,res.tld,res.subdomain,spli[1],type_value)
                            print(result)
                            if result["success"] == True:
                                messages.success(request, res.fld+' '+' '+type_value+ ' '+result["result"])
                                count_lines =count_lines+1
                                deleted = True
                            else:
                                messages.error(request, res.fld+' '+' '+type_value+ ' '+result["result"])

                            print("deleter_recordsdeleter_recordsdeleter_recordsdeleter_recordsdeleter_recordsdeleter_recordsdeleter_records")

                    else:
                        messages.error(request, spli[0]+':  Domain not found')
                except:
                    print("res is nooooooot  okaaaaaaaaaaaaay res res ")
                    messages.error(request, spli[0]+':  Domain not found (invalid  TLD !)')




              
                
                
                
                
            

            if deleted:
                messages.success(request, str(count_lines)+':  Records Deleted')

            elif added:
                messages.success(request, str(count_lines)+':  Records added')
            django_messages = []
            for message in messages.get_messages(request):
                django_messages.append({
                    "level": message.level,
                    "message": message.message,
                    "extra_tags": message.tags,
            })
                print("list of errors :")
            
                output_rerros["success"]=True
                output_rerros["data"]=django_messages
                print(output_rerros)
                print("ffffffffffffffffffff",form.errors.as_json())
        else:
            print("not ok ")
            output_rerros = {"success":False, "error":"",  "result":"","data":form.errors.as_json()}
            print(output_rerros)
            return JsonResponse(output_rerros, safe=False) 
           
        
      
          
        
        return JsonResponse(output_rerros, safe=False) 

    else:   
        print("noo one noo one")
        form = InputRecordsForm()
      
    return render(request, 'records.html', {'form':form})



# Create your views here.
@login_required
def board_topics(request,board_id):
    try:
        board_topics = Board.objects.get(pk=board_id)
        topics = board_topics.topics.order_by('last_updated').annotate(replies=Count('posts'))
       
        print(board_topics)
    except board_topics.DoesNotExist:
        raise Http404

    return render(request, 'topics.html', {'board_topics': board_topics,'topics':topics})
    
@login_required
def new_topics(request,board_id):
    try:
        board_topics = Board.objects.get(pk=board_id)
    except board_topics.DoesNotExist:
        raise Http404
    
    form = NewTopicForm(request.POST)
    

    user=User.objects.first()
    if request.method =="POST":
        if form.is_valid():    
            topic = form.save(commit=False)
            topic.board = board_topics
            topic.created_by = request.user
            topic.is_superadmin = request.user.is_superuser
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('board_topics', board_id=board_topics.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()

    return render(request, 'new_topic.html',{'board_topics': board_topics,'form':form})



''' if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        print(subject)
        print(message)
        user = User.objects.first()  # TODO: get the currently logged in user

        topic = Topic.objects.create(
            subject=subject,
            board=board_topics,
            created_by=user
        )

        post = Post.objects.create(
            message=message,
            topic=topic,
            created_by=user
        )

        return redirect('board_topics', board_id=board_topics.pk)  # TODO: redirect to the created topic page

    return render(request, 'new_topic.html',{'board_topics': board_topics})'''







@method_decorator(login_required,name="dispatch")
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message','created_by' )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', board_id=post.topic.board.pk, topic_id=post.topic.pk)





@login_required
def topic_posts(request,board_id,topic_id):
    topic = get_object_or_404(Topic,board__pk=board_id,pk=topic_id)
    topic.views += 1
    topic.save()
    return render(request,'topic_posts.html',{'topic': topic})

@login_required
def reply_topic(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.updated_by = request.user
            topic.last_updated = timezone.now()
            topic.save()
            return redirect('topic_posts', board_id=board_id, topic_id=topic_id)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})
