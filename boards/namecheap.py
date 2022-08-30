import requests,webbrowser
import xml.etree.ElementTree as ET
import xmltodict,json

        
    
class Namecheap:
 
    def __init__(self):
        print("class namecheap")
        self.error = 'aaa'

    def parseJson(self,result):
        xpars = xmltodict.parse(result)
        jsonn = json.dumps(xpars)
        result = json.loads(jsonn) 
        return result
    def request_link(self,api_link):
        response = requests.get(api_link,
        headers={"Content-Type": "application/xml"},)
        return response

    def getrecords(self,fld,domain,tld):
        print(" getrecords")
        api_link = "https://api.sandbox.namecheap.com/xml.response?ApiUser=mehdiamc&ApiKey=6453a4ecfeb945218ffc7e0da10c2733&ClientIp=160.179.244.253&UserName=mehdiamc&Command=namecheap.domains.dns.getHosts&SLD="+domain+"&TLD="+tld
        response = self.request_link(api_link)
        result = self.parseJson(response.text)
        print (result)
        output = {"success":False, "error":"",  "result":"","data":[]}
        list_of_records =[]
        if "CommandResponse" in result["ApiResponse"] and "DomainDNSGetHostsResult" in result["ApiResponse"]["CommandResponse"] and "host" in result["ApiResponse"]["CommandResponse"]["DomainDNSGetHostsResult"]:
            print("there are a Results +++++++++")
            list_of_records = result["ApiResponse"]["CommandResponse"]["DomainDNSGetHostsResult"]["host"]
            output["success"] = True 
            output["result"] = "Result Found successfully !" 
            output["data"] = list_of_records

        else:
            if result and "ApiResponse" in result and "Errors" in result["ApiResponse"] and "Error" in result["ApiResponse"]["Errors"] and "#text" in result["ApiResponse"]["Errors"]["Error"]:
                print(result["ApiResponse"]["Errors"]["Error"]["#text"])
                output["success"] = False 
                output["error"] = result["ApiResponse"]["Errors"]["Error"]["#text"]
                output["data"] = list_of_records
            
        
        
        return output
        
    
    def checkdomain(self,domain):
        domain_is =False
        api_link = "https://api.sandbox.namecheap.com/xml.response?ApiUser=mehdiamc&ApiKey=6453a4ecfeb945218ffc7e0da10c2733&ClientIp=160.179.244.253&UserName=mehdiamc&Command=namecheap.domains.getinfo&DomainName="+str(domain)+""
        response = self.request_link(api_link)
        result = self.parseJson(response.text)
        isowner=result["ApiResponse"]["CommandResponse"]["DomainGetInfoResult"]["@IsOwner"]
        if isowner == "true":
            domain_is =True
        return domain_is

    

    def setHosts(self,listrecords,domain,tld):
        output = {"success":False, "error":"",  "result":"","data":""}
        api_link= "https://api.sandbox.namecheap.com/xml.response?ApiUser=mehdiamc&ApiKey=6453a4ecfeb945218ffc7e0da10c2733&UserName=mehdiamc&ClientIp=196.64.148.10&Command=namecheap.domains.dns.setHosts&SLD="+domain+"&TLD="+tld+""
        for position,record in enumerate(listrecords):
            if record['@Name'] =="":
                record['@Name']="@"
            api_link = api_link+"&HostName"+str(position+1)+"="+record['@Name']+"&RecordType"+str(position+1)+"="+record['@Type']+"&Address"+str(position+1)+"="+record['@Address']+"&TTL"+str(position+1)+"="+str(record['@TTL'])+""
            print(position+1)
        print(api_link)
        response = self.request_link(api_link)
        result = self.parseJson(response.text)
        print(response)
        if "ApiResponse" in result and "Errors" in result["ApiResponse"] and isinstance(result["ApiResponse"]["Errors"] , dict) and "Error" in result["ApiResponse"]["Errors"] and "#text" in result["ApiResponse"]["Errors"]["Error"]:
        #or you can use if result["ApiResponse"]["Errors"] != None:    
            print(result["ApiResponse"]["Errors"]["Error"]["#text"])
            output["success"] = False 
            output["error"] = result["ApiResponse"]["Errors"]["Error"]["#text"]   
        else:       
            if "CommandResponse" in result["ApiResponse"] and "DomainDNSSetHostsResult" in result["ApiResponse"]["CommandResponse"] and "@IsSuccess" in result["ApiResponse"]["CommandResponse"]["DomainDNSSetHostsResult"]  :
                print(result["ApiResponse"]["CommandResponse"]["DomainDNSSetHostsResult"]["@IsSuccess"])
                output["success"]=True
                output["result"]="Record has been added"
        return output


    def addrecords(self,fld,domain,tld,subdomain,value,type_record,ttl):
        output = {"success":False, "error":"",  "result":"","data":""}
        resul = self.getrecords(fld,domain,tld)
        print("resulresulresulresulresulresulresul",resul)
        
        resul["data"].append({'@Name': subdomain, '@Type': type_record, '@Address': value, '@MXPref': '10', '@TTL': ttl})
        print("this is dataaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" ,resul["data"])

        
        if resul["error"] != "":
            print("result error",resul["error"])  
            output["error"]=resul["error"]
        else:
            self.setHosts(resul["data"],domain,tld)
            sethost = self.setHosts(resul["data"],domain,tld)
            if sethost["error"] != "":
                print("result error",sethost["error"])
                output["error"]=sethost["error"]
            else:
                output["success"]=True
                output["result"]=sethost["result"]
                
        return output



    def deleterecords(self,fld,domain,tld,subdomain,value,type_record):
        output = {"success":False, "error":"",  "result":"","data":""}
        resul = self.getrecords(fld,domain,tld)
        found=False
        if subdomain == "":
            subdomain="@"
        print(resul["data"])

        if resul["error"] != "":
            print("result error",resul["error"])
            output["error"]=resul["error"]
        
        else:
            for ind in resul["data"]:
                if '@Name' in ind and ind['@Name']==subdomain and '@Type' in ind and ind['@Type']==type_record and '@Address' in ind and ind['@Address']==value:
                    print("-------------------------------------->   ",ind)
                    found=True
                    resul["data"].remove(ind)
          
            if found:
                self.setHosts(resul["data"],domain,tld)
                sethost = self.setHosts(resul["data"],domain,tld)
                print("<sethost sethost sethost> ",sethost)
                if sethost["error"] == "":
                    output["success"]=True
                    output["result"]="have been Deleted"
                else:
                    print("result error",sethost["error"])
                    output["error"]=sethost["error"]
                    output["success"]=False
                    output["result"]=sethost["error"]
                    
            else:    
                output["success"]=False
                output["error"]="record Not found"
                output["result"]="record Not found"


          
            print(resul["data"])

        return output




        
        #resul["data"].append({'@Name': subdomain, '@Type': type_record, '@Address': value, '@MXPref': '10', '@TTL': '60'})
        for ind in resul["data"]:
            if '@Name' in ind and ind['@Name']==subdomain and '@Type' in ind and ind['@Type']==type_record and '@Address' in ind and ind['@Address']==value:
                print("-------------------------------------->   ",ind)
                resul["data"].remove(ind)
            else:
                print("--------------------------------------> noppp  ")
        print(resul["data"])



        
        
        

            

      #  else:
       #     if subdomain != "":
      #          sub = subdomain
       #     response = requests.get("https://api.sandbox.namecheap.com/xml.response?ApiUser=mehdiamc&ApiKey=6453a4ecfeb945218ffc7e0da10c2733&UserName=mehdiamc&ClientIp=196.64.148.10&Command=namecheap.domains.dns.setHosts&SLD="+domain+"&TLD="+tld+"&HostName1="+sub+"&RecordType1="+type_record+"&Address1="+value+"&TTL1=60",
       #    headers={"Content-Type": "application/xml"},)
        #    result = self.parseJson(response.text) 
       #     print("8794694365143543654354364",result)

       #     if "ApiResponse" in result and "Errors" in result["ApiResponse"] and isinstance(result["ApiResponse"]["Errors"] , dict) and "Error" in result["ApiResponse"]["Errors"] and "#text" in result["ApiResponse"]["Errors"]["Error"]:
            #or you can use if result["ApiResponse"]["Errors"] != None:    
        #        print(result["ApiResponse"]["Errors"]["Error"]["#text"])
        #        output["success"] = False 
         #       output["error"] = result["ApiResponse"]["Errors"]["Error"]["#text"]   
         #   else:       
          #      if "CommandResponse" in result["ApiResponse"] and "DomainDNSSetHostsResult" in result["ApiResponse"]["CommandResponse"] and "@IsSuccess" in result["ApiResponse"]["CommandResponse"]["DomainDNSSetHostsResult"]  :
           #         print(result["ApiResponse"]["CommandResponse"]["DomainDNSSetHostsResult"]["@IsSuccess"])
           #         output["success"]=True
           #         output["result"]="Record has been added"
            
                

        return output

   

















if __name__ == '__main__':
    Namecheap()



