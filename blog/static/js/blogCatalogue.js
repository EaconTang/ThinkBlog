/**
 * Created by eacon on 8/1/16.
 */
// 生成两级目录索引列表

function GenerateContentList()

{

var mainContent = $('#post_body');

var h2_list = $('#post_body h3');//如果你的章节标题不是h2,只需要将这里的h2换掉即可

if(mainContent.length < 1)

return;

if(h2_list.length>0)

{

var content = '<a name="_labelTop"></a>';

content += '<div id="navCategory">';

content += '<p style="font-size:18px"><b>目录</b></p>';

content += '<ul>';

for(var i=0; i<h2_list.length; i++)

{

var go_to_top = '<div style="text-align: right"><a href="#_labelTop">回到顶部</a><a name="_label' + i + '"></a></div>';

$(h2_list[i]).before(go_to_top);

var h3_list = $(h2_list[i]).nextAll("h3");

var li3_content = '';

for(var j=0; j<h3_list.length; j++)

{

var tmp = $(h3_list[j]).prevAll('h2').first();

if(!tmp.is(h2_list[i]))

break;

var li3_anchor = '<a name="_label' + i + '_' + j + '"></a>';

$(h3_list[j]).before(li3_anchor);

li3_content += '<li><a href="#_label' + i + '_' + j + '">' + $(h3_list[j]).text() + '</a></li>';

}

var li2_content = '';

if(li3_content.length > 0)

li2_content = '<li><a href="#_label' + i + '">' + $(h2_list[i]).text() + '</a><ul>' + li3_content + '</ul></li>';

else

li2_content = '<li><a href="#_label' + i + '">' + $(h2_list[i]).text() + '</a></li>';

content += li2_content;

}

if($('#post_body').length != 0 )

{

$($('#post_body')[0]).prepend(content);

}

}

}

GenerateContentList();