from store.models import Product
class Cart():
    def __init__(self,request):
        self.session = request.session

        # Get the current session if it exists
        cart = self.session.get('session_key')

        # if the user is new, no session key! Create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {} # both = {}

        # make sure cart is available on all pages of the site
        self.cart = cart # this cart is a local variable that doesnot exist outside of the method so we use property cart thru self.cart and assign the local variable cart to that

    def add(self, product,quantity):
        product_id = str(product.id) # convert to string because session data is stored as string
        product_qty = str(quantity)

		# Logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        # get ids from cart
        product_ids = self.cart.keys()

        # use ids to lookup products in the database model
        products = Product.objects.filter(id__in=product_ids)
        
        # return those looked up products
        return products

    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self,product,quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # get cart
        ourcart = self.cart

        # update dictionary/cart
        ourcart[product_id] = product_qty
        
        self.session.modified = True

        thing = self.cart
        return thing

    def delete(self,product):
        product_id = str(product)
        # Delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True