
# imports
from newscommunity.ncvars import *

# declarations

AD_CHANCE = 0.2

# definitions

def generateVerticalBannerAd():
    #<!-- 120x600 skyscraper; steely gaze-->
    borderColor = "CCCCCC"
    bgColor = "FFFFFF"
    linkColor = "000000"
    urlColor = "666666"
    textColor = "333333"

    data = '<div class="skyscraperAdDiv">'
    data += '''
<script type="text/javascript"><!--
google_ad_client = "pub-8797848112038141";
google_ad_width = 120;
google_ad_height = 600;
google_ad_format = "120x600_as";
google_ad_type = "text";
google_ad_channel ="";
google_color_border = "''' + borderColor + '''";
google_color_bg = "''' + bgColor + '''";
google_color_link = "''' + linkColor + '''";
google_color_url = "''' + urlColor + '''";
google_color_text = "''' + textColor + '''";
//--></script>
<script type="text/javascript"
  src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
</script>
'''
    data += '</div>\n'
    return data

def generateAdTermsBox():
    #<!-- 200x90 terms only; steely gaze-->
    borderColor = "CCCCCC"
    bgColor = "FFFFFF"
    linkColor = "000000"
    urlColor = "666666"
    textColor = "333333"

    data = '<div class="boxAdDiv">'
    data += '''
<script type="text/javascript"><!--
google_ad_client = "pub-8797848112038141";
google_ad_width = 200;
google_ad_height = 90;
google_ad_format = "200x90_0ads_al_s";
google_ad_channel ="";
google_color_border = "''' + borderColor + '''";
google_color_bg = "''' + bgColor + '''";
google_color_link = "''' + linkColor + '''";
google_color_url = "''' + urlColor + '''";
google_color_text = "''' + textColor + '''";
//--></script>
<script type="text/javascript"
  src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
</script>
'''
    data += '</div>\n'
    return data

def generateAdTermsHorizontal():
    #<!-- 468x15 terms only; steely gaze-->
    borderColor = "CCCCCC"
    bgColor = "FFFFFF"
    linkColor = "000000"
    urlColor = "666666"
    textColor = "333333"

    data = '<div class="horizontalAdDiv">'
    data += '''
<script type="text/javascript"><!--
google_ad_client = "pub-8797848112038141";
google_ad_width = 468;
google_ad_height = 15;
google_ad_format = "468x15_0ads_al";
google_ad_channel ="";
google_color_border = "''' + borderColor + '''";
google_color_bg = "''' + bgColor + '''";
google_color_link = "''' + linkColor + '''";
google_color_url = "''' + urlColor + '''";
google_color_text = "''' + textColor + '''";
//--></script>
<script type="text/javascript"
  src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
</script>
'''
    data += '</div>\n'
    return data

# classes

