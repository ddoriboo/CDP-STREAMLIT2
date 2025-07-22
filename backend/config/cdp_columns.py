"""CDP 컬럼 정의"""

CDP_COLUMNS = {
    "basic": {
        'mbr_id_no': '네이버 IDNO'
    },
    "interests": {
        'fa_int_householdsingle': '최근 1개월 1인 가구 관련 상품 결제 또는 오피스텔/원룸 거주 추정 고객',
        'fa_int_householdpet': '최근 1개월 동물용품/동물병원 결제 고객',
        'fa_int_householdchild': '최근 1개월 어린이 관련 상품 결제 고객',
        'fa_int_householdbaby': '최근 1개월 영유아 관련 상품 결제 또는 출산 정책지원금 수령 고객',
        'fa_int_householdyouth': '최근 1개월 중고등학생 관련 상품 결제 고객',
        'fa_int_publictransport': '최근 1개월 Npay 교통카드 이용 또는 교통비 결제 고객',
        'fa_int_motorcycle': '최근 1개월 오토바이 관련 상품 결제 고객',
        'fa_int_loan1stfinancial': '최근 1개월 1금융권에서 신용 대출 실행 고객',
        'fa_int_loan2ndfinancial': '최근 1개월 저축은행, 카드사, 보험사, 증권사 등에서 신용 대출을 실행 고객',
        'fa_int_loanpersonal': '최근 1개월 신용대출을 실행 고객',
        'fa_int_saving': '최근 1개월 예적금 개설 고객',
        'fa_int_jeonsemonthlyrent': '최근 24개월 계좌 및 대출이력을 통한 전월세 거주 추정 고객',
        'fa_int_homeappliance': '최근 1개월 가전 상품 결제 고객',
        'fa_int_luxury': '최근 1개월 100만원 이상 명품관련 결제 고객',
        'fa_int_delivery': '최근 1개월 식비 목적의배달 결제 고객',
        'fa_int_mutualaidservice': '최근 1개월 상조서비스 관련 결제 고객',
        'fa_int_interior': '최근 1개월 인테리어 관련 상품 결제 고객',
        'fa_int_carinsurance': '향후 1개월 자동차 보험 결제 예정으로 추정되는 고객(과거 동월 포함)',
        'fa_int_carpurchase': '최근 1개월 마이카 및 오토론을 통한 차량 구매 추정 고객',
        'fa_int_overseasshopping': '최근 1개월 해외직구 결제 고객',
        'fa_int_traveldomestic': '최근 1개월 국내여행 관련 상품 결제 고객',
        'fa_int_travelpackage': '최근 1개월 여행사 패키지 상품 결제 고객',
        'fa_int_traveloverseas': '향후 1개월 내 해외 여행 목적의 출국 예정 추정 고객',
        'fa_int_travelasia': '향후 1개월 내 아시아 지역으로 해외여행 목적의 출국 예정 추정 고객',
        'fa_int_golf': '최근 1개월 골프용품/골프장 관련 상품 결제 고객',
        'fa_int_running': '최근 1개월 러닝/마라톤 관련 상품 결제 고객',
        'fa_int_swimming': '최근 1개월 수영 관련 상품 결제 고객',
        'fa_int_pilatesyoga': '최근 1개월 필라테스/요가 관련 상품 결제 고객',
        'fa_int_gym': '최근 1개월 피트니스/헬스장 가맹점 결제 고객',
        'fa_int_wedding': '최근 1개월 결혼 준비 관련 상품 결제 및 활동 발생 고객',
        'fa_int_retirement': '향후 24개월 내 은퇴 예정으로 추정되는 고객',
        'fa_int_move': '최근 1개월 주소지 변경이력 존재 또는 이사 관련 상품 결제 고객',
        'fa_int_childbirth': '최근 1개월 임신/출산 관련 상품 결제 고객',
        'fa_int_highincome': '최근 12개월 Nice 추정소득 1억이상 고객',
        'fa_int_homeowner': '최근 12개월 주택 소유 추정 고객',
        'fa_int_business': '대출 등을 통한 사업자 추정 고객',
        'fa_int_youngprofessional': '최근 1개월 급여입금을 통해 취직 추정 고객',
        'fa_int_pharmaceutical': '최근 1개월 제약 B2B 가맹점 고객',
        'fa_int_worker': '최근 2개월 정기적으로 급여 받는 고객',
        'fa_int_fishing': '최근 1개월 낚시 관련 상품 결제 고객',
        'fa_int_diet': '최근 1개월 다이어트 목적의 상품 결제 고객',
        'fa_int_alcohol': '최근 1개월 주류 관련 상품 결제 고객',
        'fa_int_ott': '최근 1개월 OTT 관련 결제 고객'
    },
    "industries": {
        'fa_ind_education': '최근 1개월 업종>교육 결제 고객',
        'fa_ind_academy': '최근 1개월 업종>교육>학원 결제 고객',
        'fa_ind_technicacademy': '최근 1개월 업종>교육>학원>기능학원 결제 고객',
        'fa_ind_readingroom': '최근 1개월 업종>교육>학원>독서실 결제 고객',
        'fa_ind_tutoringacademy': '최근 1개월 업종>교육>학원>보습학원 결제 고객',
        'fa_ind_artsportsacademy': '최근 1개월 업종>교육>학원>예·체능계학원 결제 고객',
        'fa_ind_languageacademy': '최근 1개월 업종>교육>학원>외국어학원 결제 고객',
        'fa_ind_drivingacademy': '최근 1개월 업종>교육>학원>운전면허학원 결제 고객',
        'fa_ind_codingacademy': '최근 1개월 업종>교육>학원>프로그래밍/코딩 결제 고객',
        'fa_ind_kidsworkbookedu': '최근 1개월 업종>교육>학원>학습지교육 결제 고객',
        'fa_ind_transportation': '최근 1개월 업종>교통 결제 고객',
        'fa_ind_rentcar': '최근 1개월 업종>교통>렌터카 결제 고객',
        'fa_ind_bus': '최근 1개월 업종>교통>버스 결제 고객',
        'fa_ind_ferry': '최근 1개월 업종>교통>여객선 결제 고객',
        'fa_ind_railway': '최근 1개월 업종>교통>철도 결제 고객',
        'fa_ind_taxi': '최근 1개월 업종>교통>택시 결제 고객',
        'fa_ind_airsevice': '최근 1개월 업종>교통>항공 결제 고객',
        'fa_ind_fsc': '최근 1개월 업종>교통>항공>FSC 결제 고객',
        'fa_ind_lccair': '최근 1개월 업종>교통>항공>LCC 결제 고객',
        'fa_ind_finance': '최근 1개월 업종>금융 결제 고객',
        'fa_ind_insurance': '최근 1개월 업종>금융>보험 결제 고객',
        'fa_ind_lifeinsurance': '최근 1개월 업종>금융>보험>생명보험 결제 고객',
        'fa_ind_fireinsurance': '최근 1개월 업종>금융>보험>화재보험 결제 고객',
        'fa_ind_card': '최근 1개월 업종>금융>카드 결제 고객',
        'fa_ind_nft': '최근 1개월 업종>금융>NFT 결제 고객',
        'fa_ind_mobility': '최근 1개월 업종>모빌리티 결제 고객',
        'fa_ind_mobilitysvc': '최근 1개월 업종>모빌리티>모빌리티 서비스 결제 고객',
        'fa_ind_carwash': '최근 1개월 업종>모빌리티>모빌리티 서비스>세차장 결제 고객',
        'fa_ind_carrepairbiz': '최근 1개월 업종>모빌리티>모빌리티 서비스>자동차정비업 결제 고객',
        'fa_ind_parkinglot': '최근 1개월 업종>모빌리티>모빌리티 서비스>주차장 결제 고객',
        'fa_ind_carinterior': '최근 1개월 업종>모빌리티>모빌리티 서비스>카인테리어 결제 고객',
        'fa_ind_mobilitysales': '최근 1개월 업종>모빌리티>모빌리티 판매 결제 고객',
        'fa_ind_motobikestore': '최근 1개월 업종>모빌리티>모빌리티 판매>이륜차판매 결제 고객',
        'fa_ind_culturehobby': '최근 1개월 업종>문화/취미 결제 고객',
        'fa_ind_leisure': '최근 1개월 업종>문화/취미>레포츠시설 결제 고객',
        'fa_ind_golfcourse': '최근 1개월 업종>문화/취미>레포츠시설>골프장 결제 고객',
        'fa_ind_swimmingpool': '최근 1개월 업종>문화/취미>레포츠시설>수영장 결제 고객',
        'fa_ind_tennis': '최근 1개월 업종>문화/취미>레포츠시설>테니스 결제 고객',
        'fa_ind_fitness': '최근 1개월 업종>문화/취미>레포츠시설>피트니스 결제 고객',
        # ... 더 많은 업종 컬럼들이 있지만 일부만 포함
    },
    "scores": {
        'sc_int_householdsingle': '최근 1개월 1인 가구 관련 상품 결제 또는 오피스텔/원룸 거주 추정 고객 (예측스코어)',
        'sc_int_householdpet': '최근 1개월 동물용품/동물병원 결제 고객 (예측스코어)',
        'sc_int_householdchild': '최근 1개월 어린이 관련 상품 결제 고객 (예측스코어)',
        'sc_int_householdbaby': '최근 1개월 영유아 관련 상품 결제 또는 출산 정책지원금 수령 고객 (예측스코어)',
        'sc_int_householdyouth': '최근 1개월 중고등학생 관련 상품 결제 고객 (예측스코어)',
        'sc_int_publictransport': '최근 1개월 Npay 교통카드 이용 또는 교통비 결제 고객 (예측스코어)',
        # ... 더 많은 스코어 컬럼들
    },
    "demographics": {
        'fi_npay_age10': '연령 10대 고객',
        'fi_npay_age20': '연령 20대 고객',
        'fi_npay_age30': '연령 30대 고객',
        'fi_npay_age40': '연령 40대 고객',
        'fi_npay_age50': '연령 50대 고객',
        'fi_npay_age60': '연령 60대 고객',
        'fi_npay_ageup70': '연령 70대 고객',
        'fi_npay_gendermale': '성별 남성 고객',
        'fi_npay_genderfemale': '성별 여성 고객',
        'fi_npay_elementary': '연령 8~13세 고객',
        'fi_npay_middleschool': '연령 14~16세 고객',
        'fi_npay_highschool': '연령 17~19세 고객',
        # ... 더 많은 인구통계학적 컬럼들
    }
}

def get_all_columns():
    """모든 컬럼을 하나의 딕셔너리로 반환"""
    all_columns = {}
    for category_columns in CDP_COLUMNS.values():
        all_columns.update(category_columns)
    return all_columns

def get_columns_by_category(category: str):
    """특정 카테고리의 컬럼들을 반환"""
    return CDP_COLUMNS.get(category, {})

def get_column_description(column_name: str):
    """특정 컬럼의 설명을 반환"""
    all_columns = get_all_columns()
    return all_columns.get(column_name, "컬럼을 찾을 수 없습니다.")