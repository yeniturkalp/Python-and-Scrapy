import scrapy

class BooksSpider(scrapy.Spider): # scrapy spider yapısını oluşturur.
    name = "books" #bu değer uniq olmalıdır
    page_count = 0 #sayfa sayısı 0'dan başlatılır kodun belli sayfaya kadar okumasını sağlar 
    book_count = 1 #yazılan kitapları numaralandırır her kitapta değeri artar
    file = open("books.txt","a",encoding = "UTF-8") #bilgileri okuyup books.txt dosyası açarak içine değerleri yazar
    start_urls = [
        "https://www.kitapyurdu.com/index.php?route=product/best_sellers&page=1&list_id=1"
    ] #hangi url üzerinden işlem yapacağımızı belirtir. START_URLS ADI İLE LİSTE AÇILMASI LAZIM

    #sitede istediğimiz değerleri barındıran css kodları 
    def parse(self, response):
        book_names = response.css("div.name.ellipsis a span::text").getall() #kitap ismi bu css kodu içindeymiş
        book_authors = response.css("div.author.compact.ellipsis a::text").getall() #yazar
        book_publishers = response.css("div.publisher a span::text").getall()#yayınevi
        # book_price = response.css("div.price div.price-new span::text").getall() #fiyatı

        #değerleri okuyarak döngüye girer ve her döngüde değerleri books.txt'ye yazar
        i = 0
        while (i < len(book_names)):
            """yield {
                "name" : book_names[i],
                "author" : book_authors[i],
                "publisher" : book_publishers[i]
            }"""
            self.file.write("-----------------------------------------------\n")
            self.file.write(str(self.book_count) + ".\n")
            self.file.write("Kitap İsmi : " + book_names[i] + "\n")
            self.file.write("Yazar : " + book_authors[i] + "\n")
            self.file.write("Kitap İsmi : " + book_publishers[i] + "\n")
            # self.file.write("Fiyat : " + book_price[i] + "\n")
            self.file.write("-----------------------------------------------\n")
            self.book_count += 1
            
            i += 1
        next_url = response.css("a.next::attr(href)").get() #bir sonraki sayfaya geçişi sağlayan link
        self.page_count += 1
        
        #next url değeri boş olmayana kadar döngüye girer ve değerleri dosyaya yazdırır eğer boş olursa dosyayı kapatır.
        #120 kttabı okur ve dosyaya yazar
        if next_url is not None and self.page_count != 6:
            yield scrapy.Request(url = next_url,callback = self.parse)
        else:
            self.file.close()



