from modules import *

#***********************************************************************
#-------------------------------- Search  ---------------------------
#***********************************************************************

@user_passes_test(lambda u: u.is_staff)
@login_required
def search_all(request):
    if request.method == 'GET':
        keyword = request.GET.get('searchKeyword')
        logger.debug("Search called for keyword: %s" % keyword)
        result = global_search(keyword)
        if result:
            logger.debug("Results found")
            return  render(request, 'search_results.html', {'result':result})
        else:
            logger.debug("No Results found")
            return  render(request, 'search_results.html', {'message':'No results'})

#***********************************************************************
#-------------------------------- Home  ---------------------------
#***********************************************************************


def index(request):
    return render(request, 'Evaluator/home.html')

#***********************************************************************
# -------------------------------- Vendor ---------------------------
#***********************************************************************

@user_passes_test(lambda u: u.is_staff)
@login_required
def allVendors(request):
    return render(request, 'all_vendors.html', {'vendors': Vendors.objects.all()})

@user_passes_test(lambda u: u.is_staff)
@login_required
def vendor_details(request, vendor_pk):
    vendor = Vendor.objects.get(pk=vendor_pk)
    return render(request, 'details_vendors.html', {'vendor': vendor})
