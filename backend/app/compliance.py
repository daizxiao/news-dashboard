import logging
import json
from datetime import datetime

# Setup Audit Logger
audit_logger = logging.getLogger("AuditLogger")
audit_logger.setLevel(logging.INFO)
handler = logging.FileHandler("backend/app/audit.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
audit_logger.addHandler(handler)

class ComplianceSystem:
    def __init__(self, negative_threshold=10):
        """
        negative_threshold: Number of high-frequency negative news to trigger circuit breaker
        """
        self.negative_count = 0
        self.last_negative_time = datetime.now()
        self.is_circuit_breaker_active = False

    def log_audit(self, news_item, metadata):
        """
        Audit Log: (采集时间、来源URL、处理耗时等)
        """
        log_entry = {
            "news_id": news_item.get('id'),
            "platform": news_item.get('platform'),
            "url": news_item.get('url'),
            "collected_at": news_item.get('timestamp'),
            "processed_at": datetime.now().isoformat(),
            "metadata": metadata
        }
        audit_logger.info(json.dumps(log_entry))

    def filter_insider_info(self, text):
        """
        Pattern matching for potential insider trading keywords.
        """
        keywords = ["insider", "unpublicized", "internal info", "confidential source", "leak"]
        for kw in keywords:
            if kw in text.lower():
                return True
        return False

    def circuit_breaker_check(self, news_item):
        """
        When detecting anomalous high-frequency negative news, auto-pause or trigger warning.
        """
        # Assume impact index below -3 is highly negative
        impacts = news_item.get('sector_impacts', {})
        is_negative = any(impact < -3 for impact in impacts.values())
        
        if is_negative:
            self.negative_count += 1
            self.last_negative_time = datetime.now()
            
            # Reset count if it's been too long
            if (datetime.now() - self.last_negative_time).seconds > 60:
                self.negative_count = 1
            
            if self.negative_count >= 10: # Threshold of 10 in 60s
                self.is_circuit_breaker_active = True
                print("CIRCUIT BREAKER ACTIVATED: Anomalous negative news detected!")
                return True
        
        return False

    def manual_audit_needed(self, score):
        """
        Force manual review if AI score < 60.
        """
        return score < 60
