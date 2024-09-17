import numpy as np

def get_new_customers(time):
    """
    Generates the number of new customers who visit the site at time = time.

    Parameters
    ----------
    time: int
        The time at which to generate new customers (not currently implemented)
    
    Returns 
    ------
    n_new_visitors
        The number of new visitors to the site at the specified time

    """
    n_new_visitors = 5000
    return n_new_visitors




def predict_purchases(n, p_purchase, rng=None):
    """
    Randomly "predicts" the number of visitors to the site who actually make a purchase 
    based on the specified probability of purchase.

    Parameters
    ----------
    n: int
        The number of site visitors
    p_purchase: float
        The probability a visitor makes a purchase
    rng: numpy.random._generator.Generator, optional
        Random number generator, by default is None

    Returns
    -------
    n_purchases
        The number of the n visitors who make a purchase


    """
    if rng is None:
        rng = np.random.default_rng()
    n_purchases = np.sum(rng.binomial(1, p_purchase, n))
    return n_purchases
    

def predict_quantities(n, rng=None):
    """
    Parameters
    ----------
    n: int
        The number of purchases/sales that are made
    rng: numpy.random._generator.Generator, optional
        Random number generator, by default is None

    Returns
    -------
    total_quantity_purchased
        The total number of shirts purchased (summed across all separate sales)
    
    """
    if rng is None:
        rng = np.random.default_rng()
    #  Using a gamma(1, 2.5) distribution to approximate sales quantity
    #  Taking the ceiling so we have round numbers
    quantity_purchased = np.ceil(rng.gamma(1, 2.5, n))
    total_quantity_purchased = np.sum(quantity_purchased)
    return total_quantity_purchased
    