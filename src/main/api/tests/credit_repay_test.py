from src.main.api.models.repay_request import RepayRequest
import pytest



@pytest.mark.api
class TestCreditRepay:

    def test_credit_repay_positive(self, api_manager, create_credit_user_request, credit):
        repay_request = RepayRequest(creditId=credit.creditId,
                                     accountId=credit.id,
                                     amount=credit.amount)
        response = api_manager.user_steps.credit_repay(create_credit_user_request, repay_request)



        assert response.creditId == credit.creditId
        assert response.amountDeposited == credit.amount



    def test_credit_repay_negative(self, api_manager, create_credit_user_request, credit):
        repay_request = RepayRequest(creditId=credit.creditId,
                                     accountId=credit.id,
                                     amount=(credit.amount / 2))
        response = api_manager.user_steps.credit_repay_invalid(create_credit_user_request, repay_request)


        assert "The amount is not enough" in response.json()["error"]


