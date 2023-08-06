class UbkiReport():
    """ Класс отчет УБКИ

    Parameters
    ----------
    xml_credit_report : str
        Кредитный отчет физической особы, предпринимателя
        
    xml_credit_score : str
        Кредитный балл 

    phone : str
        Телефон 

    email : str
        Электронная почта
    """
    def __init__(self, xml_credit_report:str, xml_credit_score:str, phone:str, email:str):
        self.xml = {'report': xml_credit_report, 'score': xml_credit_score}
        self.phone = phone
        self.email = email

    def get_report_xml(self) -> str:
        """ Метод получения кредитного отчета физической особы, предпринимателя

        Returns
        -------
        ubki report : Кредитный отчет физической особы, предпринимателя
        """
        return self.xml['report']
    def get_score_xml(self) -> str:
        """ Метод получения кредитный балл

        Returns
        -------
        ubki report : Кредитний бал
        """
        return self.xml['score']