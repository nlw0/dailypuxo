import 'dart:html';
import 'dart:js';
import 'dart:async';
import 'dart:convert' show JSON;

import 'package:hashroute/hashroute.dart' as hr;

var MONTH_NAMES = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 
                    'Maio', 'Junho', 'Julho', 'Agosto',
                    'Setembro', 'Outubro', 'Novembro', 'Dezembro'];

var dailydata;
decodeDailyData(String ss) {
  dailydata = JSON.decode(ss);
}

var myimage;
var myloadingimage;
var mycaptiondate;
var mycaptiontext;
//var first_day_cell;
var active_day_cell;
var info_element;

hr.HashRouter router;
var code_to_cell = {};

var disqus_script;
var twitpic_link;
var twitter_link;
var prev_link;
var next_link;

var info_div;
var main_display_wrapper;
var image_div;

String img_uri;

void main() {
  var req = HttpRequest.getString('dailydata.json').then(decodeDailyData);
  Future.wait([req]).then((List ss) => mymain());
}

void mymain() {
  router = new hr.HashRouter();
  router.addHandlerFunc("!/:tpcode", (p, v) => dothedance(v));
  router.addHandlerFunc("!/:tpcode/", (p, v) => dothedance(v));
  router.addHandlerFunc("!/:tpcode/#:anchor", (p, v) => dothedance(v));

  DivElement cal_body = querySelector("#cal_body");
  disqus_script = querySelector("#disqus_script");

  info_div = querySelector("#info_div");
  image_div = querySelector("#image_div");
  main_display_wrapper = querySelector("#main_display_wrapper");
  info_div.remove();

  twitpic_link = querySelector("#twitpic_link");
  twitter_link = querySelector("#twitter_link");
  prev_link = querySelector("#prev_arrow");
  next_link = querySelector("#next_arrow");

  info_element = querySelector("#dp_title_info");
  info_element.onClick.listen(display_image);
  info_element.classes.toggle("info_normal", true);
  info_element.setAttribute('data-date', "info");
  info_element.onMouseEnter.listen(print_day);
  info_element.onMouseLeave.listen(clear_label);
  code_to_cell['info'] = info_element;
  
  myloadingimage = querySelector("#loading_image");
  myimage = querySelector("#main_image");
  mycaptiondate = querySelector("#main_caption_date");
  mycaptiontext = querySelector("#main_caption_text");

  DivElement month_div = new DivElement();
  month_div.classes.toggle('cal', true);
  cal_body.children.add(month_div);
  month_div.children.add(createMonth(2013, 2, first_day: 18));
  month_div.children.add(createMonth(2013, 3));
  month_div.children.add(createMonth(2013, 4));
  month_div.children.add(createMonth(2013, 5));
  month_div.children.add(createMonth(2013, 6, day_max: 16));
    
  month_div = new DivElement();
  month_div.classes.toggle('cal', true);
  cal_body.children.add(month_div);
  month_div.children.add(createMonth(2013, 6, first_day: 17, do_head:false));
  month_div.children.add(createMonth(2013, 7));
  month_div.children.add(createMonth(2013, 8));
  month_div.children.add(createMonth(2013, 9));
  month_div.children.add(createMonth(2013, 10, day_max: 20));

  month_div = new DivElement();
  month_div.classes.toggle('cal', true);
  cal_body.children.add(month_div);
  month_div.children.add(createMonth(2013, 10, first_day: 21, do_head:false));
  month_div.children.add(createMonth(2013, 11));
  month_div.children.add(createMonth(2013, 12));
  month_div.children.add(createMonth(2014, 1));
  month_div.children.add(createMonth(2014, 2, day_max: 16));

  //first_day_cell = cal_body.children[0].children[0].children[0].children[1].children[0];
  router.run();
  //router.goTo("!/2013-02-18/");
  //router.goTo("!/info/");
  if (window.location.hash=='') {
    router.goTo("!/info/");                               
  }

}

num min(num a, num b) => a<b?a:b;
    
Element createMonth(num year, num month,
                    {num first_day: 1, num day_max: 31, bool do_head:true}) {

  num day = first_day;
  var first_weekday = new DateTime(year, month, day).weekday - 1;
  var last_day = min(day_max, new DateTime(year, month + 1, 0).day);

  TableElement month_tab = new TableElement();
  month_tab.classes.toggle('cal', true);
  TableRowElement week_row;

  if (do_head) {
    month_tab.addRow().addCell()
      ..classes.toggle('cal_month_title', true)
      ..colSpan = 7
      ..text = MONTH_NAMES[month - 1] + " ${year}";
  }

  num wday = 0;
  week_row = month_tab.addRow();

  // Fill first columns until we reach the weekday form the first day to be printed.
  for(; wday < first_weekday; wday++) {
    week_row.addCell()
      ..classes.toggle('cal', true)
      ..classes.toggle('cal_blank', true);
  }
  // Print all days, until we reach the last day, creating new lines when necessary.
  for (; day <= last_day; day++, wday++) { 
    if (wday > 6){
        wday = 0;
        week_row = month_tab.addRow();
    }
    week_row.children.add(dailypuxo_day_cell(year, month, day));
  }
  // Fill remaining weekdays in last row with blanks.
  for(; wday < 7; wday++) {
    week_row.addCell()
      ..classes.toggle('cal', true)
      ..classes.toggle('cal_blank', true);
  }
  
  return month_tab; 
}

TableCellElement dailypuxo_day_cell(num year, num month, num day) {
  TableCellElement day_cell = new TableCellElement() 
      ..classes.toggle('cal', true)
      ..text = day.toString();
  day_cell.onMouseEnter.listen(print_day);
  day_cell.onMouseLeave.listen(clear_label);
  
  DateTime dt = new DateTime.utc(year, month, day);
  var cell_date = dt.toString().substring(0,10);  
  day_cell.setAttribute('data-date', "${cell_date}");
  
  if (dailydata[cell_date] != null) {
    day_cell.classes.toggle('cal_has', true);
    day_cell.onClick.listen(display_image);
    code_to_cell[cell_date] = day_cell;
  } else {
    day_cell.classes.toggle('cal_hasnt', true);
  }
  return day_cell;
}

void print_day(Event e) {
  var qq = e.target;  
  var cell_date = qq.getAttribute('data-date');
  var img_data = dailydata[cell_date];

  var label = querySelector("#o_dia");
  if (img_data != null) {
    label.text = cell_date + '\n' + img_data['message'];
  } else {
    label.text = cell_date;
  }  
}

void clear_label(Event e) {
  var label = querySelector("#o_dia");
  label.text = '';
}

void display_image(Event e) {
  var cell_date = get_date_from_cell(e.target);
  router.goTo("!/${cell_date}/");
}

void display_info(Event e) {
  router.goTo("!/info/");  
}

void dothedance(var xx){
  display_image_lower(code_to_cell[xx['tpcode']]);
}

void display_image_lower(var day_cell) {
  if (day_cell == null) {    
    return;
  }
  
  if (active_day_cell != null) {
    if(active_day_cell != info_element) {
      active_day_cell.classes.toggle('cal_active', false);  
      active_day_cell.classes.toggle('cal_has', true);  
    }
    if(active_day_cell == info_element) {
      active_day_cell.classes.toggle('info_normal', true);  
      active_day_cell.classes.toggle('info_active', false);
      unload_info_stuff();
    }
  }
  
  active_day_cell = day_cell;

  if (active_day_cell != info_element) {
    active_day_cell.classes.toggle('cal_active', true);  
    active_day_cell.classes.toggle('cal_has', false);  
    var img_data = get_img_data_from_cell(day_cell);
    replace_stuff(img_data);  
  }
  if (active_day_cell == info_element) {
    active_day_cell.classes.toggle('info_normal', false);  
    active_day_cell.classes.toggle('info_active', true);  
    load_info_stuff();
  }

}

load_info_stuff() {
  main_display_wrapper.children[0].remove();
  main_display_wrapper.children.add(info_div);
}
unload_info_stuff() {
  main_display_wrapper.children[0].remove();
  main_display_wrapper.children.add(image_div);
}

replace_stuff(var img_data){
  replace_caption(img_data);
  replace_image(img_data);
  replace_disqus(img_data);
  replace_linx(img_data);
}

replace_image(var img_data) {
  img_uri = 'http://twitpic.com/show/full/${img_data['short_id']}';
  load_puxo_image(img_uri);   
}
replace_caption(var img_data) {
  var time = DateTime.parse(img_data['local_timestamp']).toString().substring(0,19);
  mycaptiondate.text = time;
  mycaptiontext.text = img_data['message'];
}
replace_disqus(var img_data) {
  var dpid = img_data['local_timestamp'].substring(0,10);
  var newIdentifier = dpid;
  var newUrl = 'http://nwerneck.sdf.org/dailypuxo/#!/${dpid}/';
  var newTitle = dpid;
  var newLanguage = 'pt';
  var dargs = [newIdentifier, newUrl, newTitle, newLanguage];
  var point = new JsObject(context['reset'], dargs);
}
replace_linx(var img_data) {
  twitpic_link.href = "http://twitpic.com/${img_data['short_id']}";
  twitter_link.href = "http://twitter.com/nwerneck/status/${img_data['twitter_id']}";
  prev_link.href = "#!/${img_data['previous_day']}/";
  next_link.href = "#!/${img_data['next_day']}/";
}

get_date_from_cell(var td) {
  return td.getAttribute('data-date');
}

get_img_data_from_cell(var td) {
  if (td.getAttribute('data-date') == null) {
    return {"short_id":'info'};
  }
  var cell_date = td.getAttribute('data-date');
  return dailydata[cell_date];  
}




load_puxo_image(String uri) {
  myloadingimage.classes.toggle('hidden', false);  
  ImageElement image = new ImageElement(src: uri);
  image.onLoad.listen(onData, onError: onError, onDone: onDone, cancelOnError: true);
}

onData(Event e) {
  myloadingimage.classes.toggle('hidden', true);  
  myimage.src = img_uri;
}

onError(Event e) {
}

onDone() {
}

