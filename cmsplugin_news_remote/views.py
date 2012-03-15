from django.http import HttpResponse
from django.template import loader, RequestContext
from django.core.paginator import Paginator
from cmsplugin_news_remote import utils
from cmsplugin_news_remote.models import LatestNewsRemotePlugin as Plugin
from django.core.urlresolvers import reverse

def news_detail(request, **kwargs):
    template = "news_detail.html"
    
    plugin = Plugin.objects.get(id = kwargs["plugin_id"])
    latest_news = utils.get_news(plugin.get_cache_path())
    news = utils.get_archived_news(plugin.get_cache_path())
    news_object = None
    for news_item in news:
        if kwargs["slug"] == news_item.slug:
            news_object = news_item
            news_item.news_remote_link = reverse(
                'remote_news_detail',
                kwargs={'plugin_id':plugin.id, 'slug':news_item.slug})

    template_data = {
        "object":news_object,
        "latest":latest_news,
        "news_archive_link": reverse('remote_news_archive', kwargs={'plugin_id':kwargs['plugin_id']}),
    }
    template_context = RequestContext(request, template_data)
    template_filled = loader.get_template(template)
    output = template_filled.render(template_context)
    response = HttpResponse(output, mimetype=None)
    return response

def news_archive(request, **kwargs):
    template = "news_archive.html"

    plugin = Plugin.objects.get(id = kwargs["plugin_id"])
    news_list = utils.get_archived_news(plugin.get_cache_path())
    paginator = Paginator(news_list, 5)

    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1

    try:
        news = paginator.page(page)
    except (EmptyPage, InvalidPage):
        news = paginator.page(paginator.num_pages)
    template_data = {
        "news": news,
    }
    template_context = RequestContext(request, template_data)
    template_filled = loader.get_template(template)
    output = template_filled.render(template_context)
    response = HttpResponse(output, mimetype=None)
    return response
