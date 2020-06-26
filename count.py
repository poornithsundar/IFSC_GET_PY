import asyncio
import time
import aiohttp
import xlwt 
from xlwt import Workbook 
  
async def download_site(session, url):
    async with session.get(url) as response:
        s = await response.text()
        t = s[s.find('<div id="pnlDetails">'):]
        bnk =(t[t.find('<span id="lblBankName">')+23:t.find('</span>')])
        t = t.replace("</span>","",1)
        adr =(t[t.find('<span id="lblAddress">')+22:t.find('</span>')])
        t = t.replace("</span>","",1)
        ifs =(t[t.find('<span id="lblIFSCDetails">')+26:t.find('</span>')])
        print("Read {0} from {1}".format(response.content_length, url))
        return([bnk,adr,ifs])


async def download_all_sites(sites):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            task = asyncio.ensure_future(download_site(session, url))
            tasks.append(task)
        s = await asyncio.gather(*tasks, return_exceptions=True)
        return(s)

if __name__ == "__main__":
    sites = [
        "https://www.rbi.org.in/Scripts/IFSCDetails.aspx?pkid="+str(x) for x in range(1,154735)
    ]
    start_time = time.time()
    x = asyncio.get_event_loop().run_until_complete(download_all_sites(sites))
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} sites in {duration} seconds")
    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')
    sheet1.write(0,0,'BANK NAME')
    sheet1.write(0,1,'BANK ADDRESS')
    sheet1.write(0,2,'IFSC CODE')
    for i in range(1,len(x)+1):
        sheet1.write(i, 0, x[i-1][0])
        sheet1.write(i, 1, x[i-1][1])
        sheet1.write(i, 2, x[i-1][2])      
    wb.save('rbi_scrap_ifsc.xls') 
