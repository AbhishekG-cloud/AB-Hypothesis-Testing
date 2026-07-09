
def update_posterior(alpha_prior:float,beta_prior:float,conversion:int,visitors:int)->tuple[float,float]:
    if conversion < 0:
        raise ValueError("Conversions cannot be negative.")

    if visitors < 0:
        raise ValueError("Visitors cannot be negative.")

    if conversion > visitors:
        raise ValueError("Conversions cannot exceed visitors.")

    if alpha_prior <= 0 or beta_prior <= 0:
        raise ValueError("Alpha and beta must be positive.")
    alpha_post = alpha_prior+conversion
    beta_post = beta_prior + visitors - conversion

    return (alpha_post,beta_post)
def posterior_mean(alpha:float,beta:float)->float:
    if alpha <= 0 or beta <= 0:
        raise ValueError("Alpha and beta must be positive.")
    mean = alpha/(alpha+beta)

def posterior_varinace(alpha:float,beta:float)->float:
    if alpha <= 0 or beta <= 0:
        raise ValueError("Alpha and beta must be positive.")
    var = (alpha*beta)/(((alpha+beta)**2)*(alpha+beta+1))
    return var

