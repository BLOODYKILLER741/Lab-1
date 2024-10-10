import gspread
import scrapy
from datetime import datetime

class BasicSpider(scrapy.Spider):
    name = "arkansas_lottery_spider"
    start_urls = ['https://www.myarkansaslottery.com/games/instant?page=0']

    def parse(self, response):
        # Iterate through games on the main page
        for game in response.css('div.field-item'):
            game_name = game.css('h2 a::text').get()
            game_url = game.css('h2 a::attr(href)').get()

            # Follow each game's URL to scrape detailed data
            if game_url:
                full_game_url = response.urljoin(game_url)
                yield scrapy.Request(full_game_url, callback=self.parse_game_details, meta={'game_name': game_name})

        # Follow pagination to scrape all pages
        next_page = response.css('li.pager-next a::attr(href)').get() 
        if next_page is not None:
            full_next_page_url = response.urljoin(next_page)
            yield response.follow(full_next_page_url, callback=self.parse)

    def parse_game_details(self, response):
        game_name = response.meta['game_name']

        # Scraping game details
        price = response.css('div.field-name-field-ticket-price div.field-items div::text').get()
        prize_range = response.css('div.field-name-field-prize-range div.field-items div::text').get()
        odds = response.css('div.field-name-field-game-odds div.field-items div::text').get()
        game_no = response.css('div.field-name-field-game-number div.field-items div.field-item strong::text').get()
        how_to_play = response.css('section.layout-3col__left-content div.field div.field-items div.field-item p::text').get()
        last_date = response.css('p.layout-3col__col-1 span::text').get()
        start_date = response.css('p.layout-3col__col-3 span::text').get()

        # Determining game status
        status = 'ACTIVE'
        end_date = None
        if last_date != 'To Be Determined' and last_date is not None:
            end_date = datetime.strptime(last_date, '%m/%d/%Y').date()

        if start_date is not None:
            start_date_obj = datetime.strptime(start_date, '%m/%d/%Y').date()
        else:
            start_date_obj = None
        
        today_date = datetime.today().date()

        if end_date is not None and today_date > end_date:
            status = 'Ended'

        product = {
            'Game Name': game_name,
            'Cost': price,
            'Prize': prize_range,
            'Overall Odds': odds,
            'Game Number': game_no,
            'Game Description': how_to_play,
            'Status': status,
        }

        yield product

       
        self.output_to_google_sheets(product)

    def output_to_google_sheets(self, product):
        gc = gspread.service_account(filename='info.json')
        sh = gc.open('Game Data Scraper').sheet1

       
        sh.append_row([
            str(product['Game Name']),
            str(product['Cost']),
            str(product['Prize']),
            str(product['Overall Odds']),
            str(product['Game Number']),
            str(product['Game Description']),
            str(product['Status'])
        ])
