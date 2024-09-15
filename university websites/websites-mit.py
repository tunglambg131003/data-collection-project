import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import csv
import summarize

domain = "web.mit.edu/search/"
full_url = "https://web.mit.edu/search/"

def get_websites():
    profile_urls = set()

    for last_name in last_names:
        print(last_name)
        search_box = driver.find_element(By.NAME, 'q')
        search_box.clear()
        search_box.send_keys(last_name)
        search_box.submit()
        time.sleep(3)

        wait = WebDriverWait(driver, 10)

        for i in range(last_names[last_name]):
            # Parse the current page's content
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            profiles = soup.find_all('div', class_='gs-webResult')

            for profile in profiles:
                profile = BeautifulSoup(str(profile), 'html.parser')
                profile_url = profile.find('a', class_='gs-title', href=True)['href'] if profile.find('a', class_='gs-title', href=True) else None
                if profile_url:
                    profile_urls.add(profile_url)
                print("haiyaa")
            
            try:
                current_button = driver.find_element(By.CSS_SELECTOR, "div.gsc-cursor-page.gsc-cursor-current-page")
                current_page = current_button.text
                print(f"Current page: {current_page}")
                
                next_page = str(int(current_page) + 1)
                next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"div.gsc-cursor-page[aria-label='Page {next_page}'][role='link'][tabindex='0']")))

                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", next_button)

                # Wait for the new page to load
                time.sleep(3)
                print(f"Moved to page: {next_page}")
            except Exception as e:
                print(f"Error or no more pages to click: {e}")
                break
        
    return profile_urls

"""
for link in links:
        print("Processing link:", link)
        with open('text/'+local_domain+'/'+link[8:].replace("/", "_") + ".txt", "w", encoding="UTF-8") as f:
            soup = BeautifulSoup(requests.get(link).content, "html.parser")
            content = soup.get_text()
            f.write(content)
"""

def get_website_urls():
    # Re-use scraped profile URLs
    # Should update periodically
    return {'https://direct.mit.edu/isal/article/doi/10.1162/isal_a_00517/112251/Cost-efficiency-of-institutional-reward-and', 'https://mitibmwatsonailab.mit.edu/people/lam-m-nguyen/', 'https://pkgcenter.mit.edu/2020/12/07/social-impact-internships-tuyet-pham-21/', 'https://listart.mit.edu/calendar/film-screening-artist-discussion', 'https://openlearning.mit.edu/about/our-team/stephanie-tran', 'https://solve.mit.edu/users/bui-long-nghia', 'https://mitpress.mit.edu/9780262545112/the-technology-fallacy/', 'https://igutek.scripts.mit.edu/terrascope/?page=Aircapture', 'https://dspace.mit.edu/handle/1721.1/61750?show=full', 'https://mitsloan.mit.edu/staff/directory/peter-pham', 'https://studentlife.mit.edu/cac/meet-our-staff', 'https://physics.mit.edu/news/physics-students-to-attend-meeting-of-nobel-laureates/', 'https://news.mit.edu/2015/announcing-mit-shass-new-faculty-0914', 'https://www.mit.edu/~cuongng/uploads/resume.pdf', 'https://solve.mit.edu/users/trung-nguyen-1', 'https://psoc.mit.edu/investigators/ntran', 'https://www.mit.edu/~cuongng/tag/rbm/', 'https://sites.mit.edu/freddytn/author_biblio/pham-crystal/', 'https://cmsw.mit.edu/portable-postsocialisms-new-cuban-mediascapes-after-the-end-of-history/', 'https://dspace.mit.edu/handle/1721.1/105896?show=full', 'https://betterworld.mit.edu/spectrum/issues/spring-2021/a-financial-aid-success-story/', 'https://acl.mit.edu/people/nghiaht', 'https://www.media.mit.edu/people/stnguyen/overview/', 'https://internetpolicy.mit.edu/team/viet-tran-nguyen/', 'https://oge.mit.edu/msrp/profiles/suong-tran/', 'https://news.mit.edu/2022/mit-student-club-engineers-without-borders-works-village-tanzania-1017', 'https://sites.mit.edu/freddytn/?query-18-page=3&cst', 'https://idm.mit.edu/student/anna-maria-phan/', 'https://mcgovern.mit.edu/2021/09/09/new-programmable-gene-editing-proteins-found-outside-of-crispr-systems/', 'https://pkgcenter.mit.edu/2023/04/12/pkg-service-spotlight-alumna-discovers-lifelong-connection-to-service-during-fellowship/', 'https://www.media.mit.edu/posts/golda-nguyen-and-jack-reid-awarded-soffen/', 'https://mitsloan.mit.edu/staff/directory/mimi-phan', 'https://jmlr.csail.mit.edu/proceedings/papers/v48/bui16.html', 'https://studentlife.mit.edu/news/harnessing-power-citizens', 'https://vpf.mit.edu/long-tran', 'https://qigroup.mit.edu/testing-page/', 'https://superurop.mit.edu/scholars/tuan-manh-phan/', 'https://sites.mit.edu/freddytn/author_biblio/rowland-kendrith-m/', 'https://calendar.mit.edu/trantv79_645', 'http://web.mit.edu/ccclab/members/hoang/index.html', 'https://www.mit.edu/~cuongng/project/uqml3/', 'http://www.mit.edu/~esontag/PUBDIR/Author/NGUYEN-T.html', 'https://news.mit.edu/2005/vietnamese-guitar-show-strikes-5-venoms', 'https://cmsw.mit.edu/event/paloma-duong-portable-postsocialisms-postsocialismos-de-bolsillo/', 'https://direct.mit.edu/dint/article-abstract/3/2/336/98240', 'https://chemistry-buchwald.mit.edu/people/christine-nguyen-1', 'https://solve.mit.edu/users/lien-nguyen', 'https://solve.mit.edu/users/tuan-nguyen', 'https://lemelson.mit.edu/award-winners/kayla-nguyen', 'https://dspace.mit.edu/handle/1721.1/7758/browse?authority=01cc50938a035d1cf2a67859371479a1&type=author', 'https://sites.mit.edu/freddytn/', 'https://direct.mit.edu/dint/article-abstract/3/4/606/107672', 'https://mitpress.mit.edu/author/hoa-pham-38758/', 'https://sites.mit.edu/freddytn/?query-18-page=4', 'https://dspace.mit.edu/bitstream/handle/1721.1/87274/51480483-MIT.pdf', 'https://www.mit.edu/~cuongng/publication/pub48/', 'https://solve.mit.edu/users/viet-lac', 'https://physicaleducationandwellness.mit.edu/instructor/jinny-dang/', 'https://solve.mit.edu/users/hai-nguyen', 'https://oge.mit.edu/msrp/profiles/vu-anh-le/', 'https://calendar.mit.edu/epham_31', 'http://web.mit.edu/mas.110/www/2006/fade_gallery/Tran_Bao.html', 'http://web.mit.edu/nsl/www/', 'https://people.csail.mit.edu/qmn/', 'https://solve.mit.edu/users/duyen-nguyen', 'https://sites.mit.edu/freddytn/author_biblio/ding-huafeng/', 'https://vismod.media.mit.edu/people/affiliates/bui.html', 'https://news.mit.edu/2023/four-researchers-mit-ties-earn-schmidt-science-fellowships-0512', 'https://news.mit.edu/2016/student-profile-lily-bui-1013', 'https://calendar.mit.edu/event/thesis_defense_ellen_duong', 'https://gilliardlab.mit.edu/members/', 'https://alumic.mit.edu/redirect.aspx?linkID=7222771&sendId=2447843&eid=612240&gid=13', 'https://calendar.mit.edu/event/thesis_defense_-_brandon_tran', 'https://www.onelab.mit.edu/team', 'https://sites.mit.edu/freddytn/biblio/three-dimensional-visualization-lymph-node-morphology-using-oct/', 'https://people.csail.mit.edu/hubert/thesis/hubert-phd-thesis.pdf', 'https://news.mit.edu/2021/dendritic-t-cells-tumors-1119', 'https://calendar.mit.edu/event/infinite-dimensional-algebra-seminar-do-kien-hoang-yale', 'https://math.mit.edu/~dav/LG/abstracts19/Nov27.pdf', 'https://www.mit.edu/~cuongng/project/hdg1/', 'https://projects.csail.mit.edu/jacm/Authors/buithangnguyen.html', 'https://jamisongroup.mit.edu/author/tho-tran-ph.d.-19/', 'https://direct.mit.edu/edfp/article-abstract/9/4/515/10218', 'https://mitpress.mit.edu/9780262551861/trans-technologies/', 'https://direct.mit.edu/rest/article/83/3/498/57274/Environmental-Regulation-and-Productivity-Evidence', 'https://dusp.mit.edu/people/delia-wendel', 'https://architecture.mit.edu/people/ai-bui', 'https://solve.mit.edu/users/isabella-duong', 'https://biology.mit.edu/biogenesis-podcast-thy-pham/', 'https://www.mit.edu/~cuongng/tag/hdg/', 'https://dspace.mit.edu/handle/1721.1/107673', 'https://calendar.mit.edu/thuynh09_681/calendar', 'https://sites.mit.edu/freddytn/author_biblio/boppart-stephen-a/', 'https://jmlr.csail.mit.edu/proceedings/papers/v32/nguyenb14.html', 'https://ceepr.mit.edu/people/tran-tony/', 'https://chemistry.mit.edu/henry-tran-graduate-student/', 'https://ksj.mit.edu/event/seminar-kim-vy-tran-on-galaxies-and-cosmology/', 'https://quantumgas.mit.edu/people/', 'https://www.ll.mit.edu/about/laboratory-stories/huy-nguyen', 'http://web.mit.edu/nsl/www/preprints/stochastic_contraction09.pdf', 'https://news.mit.edu/2015/harper-kenausis-lowder-tran-win-doe-support-0810', 'https://biology.mit.edu/staff/pham-martha/', 'https://sites.mit.edu/freddytn/biblio/fourier-transform-light-scattering-ftls-cells-and-tissues/', 'https://sites.mit.edu/freddytn/author_biblio/suslick-kenneth-s/', 'https://cheme.mit.edu/people-post/huu-khiem-nguyen/', 'http://hjkgrp.mit.edu/author/tuan-anh-pham/', 'https://www.ll.mit.edu/biographies/bich-t-vu', 'https://dspace.mit.edu/bitstream/handle/1721.1/78574/18-100c-spring-2006/contents/projects/duong.pdf', 'https://cmsw.mit.edu/profile/lily-bui/', 'https://camp.smart.mit.edu/events/smart-camp-seminar-series-tessa-therapeutics-by-dr-dang-l-vu-tessa-therapeutics', 'https://drennan.mit.edu/index.php/current-graduate-students/alexander-duong/', 'https://news.mit.edu/2019/celebrating-four-years-mindhandheart-1218', 'https://direct.mit.edu/rest/article/85/3/693/57447/Regulation-and-Capitalization-of-Environmental', 'https://direct.mit.edu/glep/article/9/4/136/14756/The-Sustainability-Debate-Deja-Vu-All-Over-Again', 'https://jmlr.csail.mit.edu/proceedings/papers/v37/hoang15.html', 'https://calendar.mit.edu/andrew0_420', 'https://qce.mit.edu/people.html', 'https://solve.mit.edu/users/huynh-tuyet', 'https://dspace.mit.edu/handle/1721.1/107219', 'https://www.psfc.mit.edu/people/visiting-scientists/kim-chinh-tran', 'https://sites.mit.edu/freddytn/author_biblio/johnson-patricia-a/', 'https://science.mit.edu/sciences-covid-19-heroes/', 'https://direct.mit.edu/jcws/article/13/1/60/13197/Nhan-Van-Giai-Ph-m-and-Vietnamese-Reform-Communism', 'https://www.mit.edu/~cuongng/project/cfd4/', 'https://solve.mit.edu/users/nguyen-bao-nguyen-huu', 'https://cmsw.mit.edu/event/lily-bui-warning-systems-disaster-risk-reduction-island-city/', 'https://dspace.mit.edu/handle/1721.1/113033?show=full', 'https://www.ll.mit.edu/about/laboratory-stories/stephanie-tran', 'https://www.gear.mit.edu/jimmy-tran', 'https://languages.mit.edu/events/walking-meditation-led-by-sister-dang-nghiem-and-sister-truc-nghiem/', 'https://groups.csail.mit.edu/medg/ftp/pham/PhamMaiPhuong-meng-eecs-2020.pdf', 'https://amr.smart.mit.edu/staff-and-students/pham-hoang-long', 'https://direct.mit.edu/netn/article/5/3/666/98350/A-morphospace-of-functional-configuration-to', 'https://lbgtq.mit.edu/trans', 'https://news.mit.edu/2017/hybrid-drones-carry-heavier-payloads-greater-distances-0804', 'https://dspace.mit.edu/handle/1721.1/7582/browse?authority=2961859b7798f59ffc6feb5c1b3edd13&type=author', 'https://www.media.mit.edu/posts/time-100-next-2019/', 'https://fraenkel.mit.edu/people/', 'https://dusp.mit.edu/spurs-fellows/truc-nguyen', 'https://solve.mit.edu/users/tra-my-nguyen', 'https://superurop.mit.edu/scholars/phuong-mai-pham/', 'https://solve.mit.edu/users/melanie-tran', 'https://stuff.mit.edu/afs/athena.mit.edu/reference/rfc/pdfrfc/rfc5758.txt.pdf', 'https://swagergroup.mit.edu/news/tran-suchol-and-intaks-work-published-journal-polymer-science-part-polymer-chemistry', 'https://jmlr.csail.mit.edu/proceedings/papers/v32/tang14.html', 'https://direct.mit.edu/isal/article/doi/10.1162/isal_a_00568/116851/Optimisation-of-hybrid-institutional-incentives', 'https://chemistry-buchwald.mit.edu/people/hanh-nguyen', 'https://sites.mit.edu/freddytn/author_biblio/boppart-stephen-a/page/2/', 'https://web.mit.edu/almlab/lttu_nguyen.html', 'https://www.media.mit.edu/people/a.nguyen/updates/', 'https://calendar.mit.edu/event/thesis-defense-gefei-dang', 'https://camp.smart.mit.edu/team/nguyen-tan-dai', 'https://solve.mit.edu/users/tran-tan-linh', 'https://news.mit.edu/2024/3-questions-paloma-duong-complexities-cuban-culture-book-0214', 'https://mitpress.mit.edu/author/anh-nguyen-phillips-28452/', 'https://sites.mit.edu/freddytn/author_biblio/popescu-gabriel/', 'https://vpf.mit.edu/crystal-nguyen', 'https://dusp.mit.edu/spurs-fellows/mai-thi-nguyen', 'https://web.mit.edu/nse/news/spotlights/2020/thanh-nguyen.html', 'https://mitpress.mit.edu/author-talk-the-transformation-myth-by-gerald-c-kane-rich-nanda-anh-nguyen-phillips-and-jonathan-r-copulsky/', 'https://listart.mit.edu/exhibitions/jun-nguyen-hatsushiba-memorial-project-nha-trang-vietnam-towards-complex-courageous', 'https://idss.mit.edu/staff/amy-huynh/', 'https://ogc.mit.edu/latest/highest-court-massachusetts-sides-mit-student-suicide-lawsuit', 'https://solve.mit.edu/users/felix-duong', 'https://officesdirectory.mit.edu/cmsw', 'https://sites.mit.edu/freddytn/biblio/fourier-transform-light-scattering-inhomogeneous-and-dynamic-structures/', 'https://mitpressbookstore.mit.edu/book/9798886660449', 'https://jmlr.csail.mit.edu/papers/v18/16-603.html', 'https://news.mit.edu/2017/monica-pham-advancing-nuclear-power-and-empowering-girls-0421', 'https://sites.mit.edu/freddytn/editor/raghavachari-ramesh/', 'https://internetpolicy.mit.edu/05-17-2023-internet-policy-research-initiative-policy-and-pizza-series-presents-chief-technology-officer-u-s-federal-trade-commission/', 'https://micromasters.mit.edu/fin/team/', 'https://dspace.mit.edu/handle/1721.1/55140?show=full', 'https://mitpress.mit.edu/9781913380618/empathy/', 'https://www.media.mit.edu/people/gnguyen/overview/', 'https://cmsw.mit.edu/tag/paloma-duong/', 'https://dspace.mit.edu/handle/1721.1/54684', 'https://jmlr.csail.mit.edu/proceedings/papers/v48/hoang16.html', 'https://solve.mit.edu/users/natalie-tran', 'https://esp.mit.edu/teach/teachers/vduong/bio.html', 'https://betterworld.mit.edu/scholarships-at-mit-hung-huynh-24/huynh-hung-edit-web-01/', 'https://calendar.mit.edu/event/physics_phd_thesis_defense_huy_duc_phan', 'https://www.media.mit.edu/people/stnguyen/updates/', 'https://globalchange.mit.edu/about-us/personnel/tran-tony', 'https://alum.mit.edu/slice/data-wind-and-waves-guarding-against-disaster', 'https://cmsw.mit.edu/tag/lily-bui/', 'https://betterworld.mit.edu/scholarships-at-mit-hung-huynh-24/', 'https://superurop.mit.edu/scholars/hoang-nguyen/', 'https://news.mit.edu/2020/no-pause-pandemic-student-researchers-nuclear-science-engineering-0818', 'https://direct.mit.edu/isal/article/doi/10.1162/isal_a_00153/99162/On-the-Expected-Number-and-Distribution-of', 'https://direct.mit.edu/netn/issue/5/3', 'https://ocw.mit.edu/courses/24-961-introduction-to-phonology-fall-2014/resources/mit24_961f14_pset7/', 'https://cdo.mit.edu/blog/2021/11/15/female-disruptors-nhat-nguyen-of-autonomous-ai-on-the-three-things-you-need-to-shake-up-your-industry/', 'https://www.mit.edu/~tdn/', 'https://mitcommlab.mit.edu/nse/fellows_staff/monica-pham/', 'https://haiti.mit.edu/nguyen-dang-trien/', 'https://lit.mit.edu/avery-nguyen-22/', 'https://sites.mit.edu/freddytn/?query-18-page=2&cst', 'https://math.mit.edu/research/highschool/primes/materials/2018/conf/14-1%20Pham.pdf', 'https://dspace.mit.edu/handle/1721.1/131023/browse?authority=66c9bfda270605faea8af2604187f0d9&type=author', 'https://mitsloan.mit.edu/staff/directory/truc-nguyen', 'https://sites.mit.edu/freddytn/author_biblio/chaney-eric-j/', 'https://physics.mit.edu/news/total-effervescence-princeton-community-remembers-minh-thi-nguyen-21/', 'https://direct.mit.edu/artm/article/6/2/27/18029/Homebound-The-Art-of-Public-Space-in-Contemporary', 'https://www.media.mit.edu/people/nguyet11/overview/', 'https://mitpress.mit.edu/author/lucky-tran-29566/', 'https://languages.mit.edu/culture-and-media-in-contemporary-cuba/', 'https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00351/97775/Revisiting-Multi-Domain-Machine-Translation', 'https://systems.mit.edu/team/jimmy-tran/', 'https://listart.mit.edu/calendar/preview-list-projects-26-alison-nguyen', 'https://www.mit.edu/~cuongng/project/hyper2/', 'https://dspace.mit.edu/handle/1721.1/99509', 'https://direct.mit.edu/rest/article/92/1/166/57797/Trading-on-Time', 'https://jmlr.csail.mit.edu/proceedings/papers/v37/pham15.html', 'https://ras.mit.edu/about-ras/staff-directory/ai-nguyen', 'https://civic.mit.edu/author/katie-arthur/index.html', 'https://cmsw.mit.edu/profile/paloma-duong/', 'https://pkgcenter.mit.edu/2024/05/14/social-impact-internships-dat-tran-27/', 'https://sites.mit.edu/freddytn/author_biblio/kotynek-jan-g/', 'https://glimpsepod.scripts.mit.edu/home/2015/12/02/episode-4-le-nguyen-hoang/', 'https://direct.mit.edu/isal/article/doi/10.1162/isal_a_00281/98404/The-effect-of-mutation-on-equilibrium-properties', 'https://www.mit.edu/~cuongng/project/cem3/', 'https://www.mit.edu/~cuongng/publication/pub4/', 'https://oge.mit.edu/msrp/profiles/nga-vu/', 'https://sites.mit.edu/freddytn/author_biblio/zysk-adam-m/', 'https://dspace.mit.edu/handle/1721.1/105460', 'https://wi.mit.edu/news/meet-whitehead-postdoc-han-tran', 'https://meche.mit.edu/people/staff/sacollin@mit.edu', 'https://civic.mit.edu/index.html%3Fp=981.html', 'https://credentials.professional.mit.edu/b8eb0de8-e27d-4ed1-ac4c-5955d30c4549', 'https://solve.mit.edu/users/pham-huy-cuong', 'https://languages.mit.edu/events/sister-dang-nghiem-speaks-on-mindfulness-as-medicine/', 'https://sites.mit.edu/freddytn/biblio/mit-covid-19-datathon-data-without-boundaries/', 'https://bcs.mit.edu/directory/kathy-tran', 'https://imes.mit.edu/people/tran-nancy', 'https://open.mit.edu/profile/01H2AJW2A4GFJ1M2FD7ARH3W77/', 'https://chaobuddhism.mit.edu/2019-sister-dang-nghiem', 'https://direct.mit.edu/netn/article/5/3/646/97541/Toward-an-information-theoretical-description-of', 'https://direct.mit.edu/asep/article/14/2/66/16982/Comments-by-Vu-Quoc-Huy-on-The-Impact-of', 'https://pda.mit.edu/2015/05/15/featured-postdoc-seminar-speaker-dr-le-nguyen-hoang/', 'http://hjkgrp.mit.edu/author/anh-nguyen/', 'https://calendar.mit.edu/sthuynhmath_732', 'https://web.mit.edu/nse/news/spotlights/2017/monica-pham.html', 'https://mitpress.mit.edu/9780262544894/trap-door/', 'https://wi.mit.edu/news/meet-whitehead-postdoc-anh-nguyen', 'https://news.mit.edu/2016/integrating-user-collected-data-city-planning-lily-bui-0826', 'https://www.ll.mit.edu/news/intern-spotlight-viet-tran-gains-hands-engineering-experience-helping-robots-work-together', 'https://dspace.mit.edu/handle/1721.1/139473', 'https://engineering.mit.edu/fellows/tam-nguyen/', 'https://mitcommlab.mit.edu/nse/fellows_staff/marina-dang/', 'https://idm.mit.edu/student/chinh-bui/', 'https://www.media.mit.edu/people/a.nguyen/overview/', 'https://pkgcenter.mit.edu/2016/12/13/iap-17-lily-bui-phd/', 'https://dspace.mit.edu/handle/1721.1/127803', 'https://superurop.mit.edu/scholars/huy-dang-pham/', 'https://direct.mit.edu/books/oa-monograph/5770/chapter/4729095/A-Sense-of-Deja-Vu', 'https://economics.mit.edu/sites/default/files/2022-10/NGUYEN_ThiMaiAnh_cv.pdf', 'https://solve.mit.edu/users/hoang-doan', 'https://bioelectronics.mit.edu/author/thang-pham/', 'https://jshun.csail.mit.edu/6506-s24/lectures/lecture4-2.pdf', 'https://jmlr.csail.mit.edu/proceedings/papers/v32/hoang14.html', 'https://superurop.mit.edu/scholars/thuy-duong-vuong/', 'https://wi.mit.edu/news/meet-whitehead-postdoc-ally-nguyen', 'https://community.appinventor.mit.edu/t/rotating-imagesprite-on-meter-display/41568', 'https://solve.mit.edu/users/-91549', 'https://jmlr.csail.mit.edu/proceedings/papers/v25/than12.html', 'https://people.csail.mit.edu/dfhuynh/research/thesis/thesis.html', 'https://sites.mit.edu/freddytn/author_biblio/bellafiore-frank-j/', 'https://sloanreview.mit.edu/article/how-to-manage-alliances-strategically/', 'https://www.mit.edu/~cuongng/project/cem7/', 'https://wi.mit.edu/news/evolutionary-d-j-vu', 'https://www.ll.mit.edu/biographies/trang-nguyen', 'https://mit-eesg.github.io/author/edward-nguyen/', 'https://chemistry-buchwald.mit.edu/people/john-nguyen', 'https://openlearning.mit.edu/about/our-team/giang-jenny-bui', 'https://vpf.mit.edu/long-tran-named-assistant-controller', 'https://people.csail.mit.edu/dfhuynh/research/research.html', 'https://languages.mit.edu/student-awards/the-isabelle-de-courtivron-writing-prize/2021-de-courtivron-writing-prize/', 'https://web.mit.edu/lmf/www/member_pages/2024.html', 'https://mitsloan.mit.edu/staff/directory/stephanie-tran', 'https://listart.mit.edu/sites/default/files/media/documents/2023-02/mit-listprojects-nguyen_final_accessible.pdf', 'https://mitpress.mit.edu/9781913380823/the-other-shore/', 'https://jmlr.csail.mit.edu/proceedings/papers/v28/ouyang13.html', 'https://calendar.mit.edu/dang20v_106', 'https://openlearning.mit.edu/about/our-team/duyen-nguyen', 'https://bcs.mit.edu/directory/trang-pham', 'https://mitpressbookstore.mit.edu/book/9789819980024', 'https://dspace.mit.edu/handle/1721.1/75816?show=full', 'https://news.mit.edu/2017/mapathon-directing-humanitarian-aid-to-puerto-rico-1016', 'https://physics.mit.edu/news/in-remembrance-minh-thi-nguyen/', 'https://people.csail.mit.edu/thurston/', 'https://betterworld.mit.edu/scholarships-at-mit-new-voices/', 'https://www.mit.edu/~cuongng/', 'https://listart.mit.edu/exhibitions/list-projects-26-alison-nguyen', 'https://www.ll.mit.edu/biographies/linh-pham', 'https://discovery-patsnap-com.libproxy.mit.edu/company/sao-thai-duong-joint-stock-company/patent/', 'https://ctl.mit.edu/about/bio/anh-nguyen', 'https://oge.mit.edu/dang-you-live-in-tang/', 'https://biology.mit.edu/tile/thy-pham/', 'https://cre.mit.edu/people/viet-nguyen/', 'https://dspace.mit.edu/handle/1721.1/35285?show=full', 'https://www.ccc.mit.edu/person/thanh-mai-phan/', 'https://solve.mit.edu/users/thi-pham', 'https://cmsw.mit.edu/paloma-duong-homebound-the-art-of-public-space-in-contemporary-cuba/', 'https://wi.mit.edu/multimedia/biogenesis-podcast-thy-pham-bartel-lab-applying-neural-nets-rna-biology', 'https://calendar.mit.edu/tongdang_333/calendar', 'https://www.gas-turbine-lab.mit.edu/research-projects/project-one-29xj5-xy9wm', 'https://microbiome.mit.edu/tag/le-thanh-tu-nguyen/', 'https://bcs.mit.edu/directory/david-nguyen', 'https://spranger-lab.mit.edu/news', 'https://direct.mit.edu/dint/article-abstract/3/4/578/107428', 'https://news.mit.edu/2019/buddhist-sister-dang-nghiem-invites-mit-community-to-practice-mindfulness-0315', 'https://wi.mit.edu/news/ngoc-han-tran-chosen-howard-hughes-medical-institute-be-hanna-gray-fellow', 'https://cmsw.mit.edu/event/fall-2016-alumni-panel-andres-lombana-bermudez-colleen-kaman-abe-stein-and-lily-bui/', 'https://cdo.mit.edu/blog/2021/03/22/career-stories-thuy-anh-vu-sfmba-2021/', 'https://www.psfc.mit.edu/news/multimedia/2017/monica-pham-advancing-nuclear-power-and-empowering-girls', 'https://cse.mit.edu/people/n-cuong-nguyen/', 'https://news.mit.edu/2020/mit-students-explore-pandemic-response-through-coded-simulation-1207', 'https://giving.mit.edu/cat-si-dang-le-1998-and-hong-van-minh-le-2000-fund', 'https://solve.mit.edu/users/-83506', 'https://studentlife.mit.edu/cac/meet-our-staff/sandy-hoang', 'https://languages.mit.edu/new-faces/', 'https://www.mit.edu/~ngutt/', 'https://pkgcenter.mit.edu/2023/11/08/pkg-ideas-alum-anh-vu-sawyer-featured-in-oprah-daily/'}
    
    # # Return links that are likely to include profile information
    # return {https://mitibmwatsonailab.mit.edu/people/lam-m-nguyen/, }


last_names = {
    'Bui': 3,
    'Dang': 2,
    'Duong': 4,
    'Hoang': 2,
    'Huynh': 1,
    'Nguyen': 10,
    'Pham': 5, # Are you a robot?
    'Phan': 1,
    'Tran': 4,
    'Vu': 1
}

# Run Chrome in the background

# Step 1: Set up ChromeOptions and its arguments
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")  # Add this if running in Docker or Linux environments
chrome_options.add_argument("--disable-dev-shm-usage")  # Required for running in some systems
chrome_options.add_argument("--window-size=1920x1080")

# Step 2: Change the page load strategy to none
chrome_options.page_load_strategy = 'none'  # Avoid full page load

# Step 3: Initialize the WebDriver with merged options
driver = webdriver.Chrome(options=chrome_options)
# Step 4: Navigate to a URL
driver.get(full_url)

# Step 5: Perform actions on the page
wait = WebDriverWait(driver, 20)
element = wait.until(EC.presence_of_element_located((By.NAME, 'q')))
driver.execute_script("window.stop();")

# website_urls = get_websites() # Enable if need re-scraping
website_urls = get_website_urls() # Enable if reusing scraped profile URLs
print("Profiles URLs:", website_urls)

driver.quit()
print("hello")

with open('university websites/profiles/websites-mit.csv', 'w', newline='') as file_output:
    headers = ['Website Summary', 'Website URL']
    writer = csv.DictWriter(file_output, fieldnames=headers)
    writer.writeheader()

    for website_url in website_urls:
        website_content = requests.get(website_url, timeout=30).content # Set a 30-second timeout
        soup = BeautifulSoup(website_content, 'html.parser')

        # Extract text from the website and summarize it
        website_content = soup.get_text()
        website_summary = summarize.summarize_text(website_content, 75, 25)

        print(f"Website Summary of {website_url} is: {website_summary}")
        writer.writerow({
            'Website Summary': website_summary.strip(),
            'Website URL': website_url
        })

print("Done and dusted!")