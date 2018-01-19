import json
import urllib.parse
import urllib.request

from django.core.files.storage import default_storage
from django.http import Http404
from django.shortcuts import redirect
# Create your views here.
from django.template.response import TemplateResponse
from django.urls import reverse

from bioconvertapi.wrappers import get_job_info_from_identifier, BioconvertWrapper
from bioconvertwebui.forms import FormIdentifier, FormFile, FormURL


def index(request):
    form_identifier = None
    form_file = None
    form_url = None
    is_file = False
    is_url = False
    is_identifier = False
    if request.method == "POST":
        if request.POST["key"] == "identifier":
            is_identifier = True
            form_identifier = FormIdentifier(data=request.POST)
            if form_identifier.is_valid():
                return redirect('bioconvertwebui:results', identifier=form_identifier.cleaned_data['identifier'])
        if request.POST["key"] == "url":
            is_url = True
            form_url = FormURL(data=request.POST)
            if form_url.is_valid():
                data = dict(
                    input_url=request.POST["input_url"],
                    postpone_conversion=True
                )
                data = urllib.parse.urlencode(data)
                data = data.encode('ascii')  # data should be bytes
                filename, headers = urllib.request.urlretrieve(
                    url=request.build_absolute_uri(reverse(
                        'bioconvertapi:bioconvert',
                        kwargs=dict(
                            input_format=request.POST["input_format"],
                            output_format=request.POST["output_format"]),
                    )),
                    data=data,
                )
                response = json.loads(open(filename, "r").read())
                return redirect('bioconvertwebui:results', identifier=response['identifier'])
        if request.POST["key"] == "file":
            is_file = True
            form_file = FormFile(request.POST, request.FILES)
            if form_file.is_valid():
                data = dict(
                    input_file=request.FILES['input_file'],
                    input_format=request.POST["input_format"],
                    output_format=request.POST["output_format"],
                    postpone_conversion=True,
                )
                response = BioconvertWrapper().run_computation(
                    request=request,
                    data=data,
                )
                return redirect('bioconvertwebui:results', identifier=response['identifier'])
    if form_identifier is None:
        form_identifier = FormIdentifier()
    if form_url is None:
        form_url = FormURL()
    if form_file is None:
        form_file = FormFile()
    context = dict(
        form_identifier=form_identifier,
        form_url=form_url,
        form_file=form_file,
        is_fresh=not is_file and not is_identifier and not is_url,
        is_file=is_file,
        is_identifier=is_identifier,
        is_url=is_url,
    )
    return TemplateResponse(request, 'bioconvertwebui/index.html', context)


def results(request, identifier):
    try:
        job_info = get_job_info_from_identifier(identifier)
    except FileNotFoundError:
        raise Http404
    context = dict(
        status=job_info["status"],
        identifier=identifier,
        input_format=job_info["input_format"],
        input_filename=job_info["input_filename"],
        output_format=job_info["output_format"],
        output_url=job_info["output_url"],
        error_message=job_info["error_message"],
        absolut_url=request.build_absolute_uri(reverse('bioconvertwebui:results', args=[identifier])),
    )
    return TemplateResponse(request, 'bioconvertwebui/results.html', context)
