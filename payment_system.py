"""
Система платежей для бота
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
# YooMoney removed - using Telegram Stars only
from logger import bot_logger

class PaymentType(Enum):
    """Типы платежей"""
    PREMIUM_SUBSCRIPTION = "premium_subscription"
    HEARTS_PACK = "hearts_pack"
    PREMIUM_FEATURES = "premium_features"
    DONATION = "donation"

@dataclass
class PaymentPlan:
    """План платежа"""
    id: str
    name: str
    description: str
    amount: float
    currency: str = "RUB"
    payment_type: PaymentType = PaymentType.HEARTS_PACK
    benefits: List[str] = None
    duration_days: int = 0  # 0 = разовый платеж
    
    def __post_init__(self):
        if self.benefits is None:
            self.benefits = []

class PaymentPlans:
    """Доступные планы платежей"""
    
    PLANS = {
        "premium_month": PaymentPlan(
            id="premium_month",
            name="⭐ Премиум подписка",
            description="Премиум подписка на 30 дней",
            amount=169.0,
            payment_type=PaymentType.PREMIUM_SUBSCRIPTION,
            benefits=[
                "Неограниченные сообщения", 
                "Приоритетная поддержка", 
                "Эксклюзивные функции",
                "Доступ к играм и развлечениям",
                "Персонализация бота"
            ],
            duration_days=30
        )
    }
    
    @classmethod
    def get_plan(cls, plan_id: str) -> Optional[PaymentPlan]:
        """Получает план по ID"""
        return cls.PLANS.get(plan_id)
    
    @classmethod
    def get_plans_by_type(cls, payment_type: PaymentType) -> List[PaymentPlan]:
        """Получает планы по типу"""
        return [plan for plan in cls.PLANS.values() if plan.payment_type == payment_type]
    
    @classmethod
    def get_all_plans(cls) -> List[PaymentPlan]:
        """Получает все планы"""
        return list(cls.PLANS.values())

class PaymentProcessor:
    """Процессор платежей"""
    
    def __init__(self):
        # Payment manager removed - payments now handled via Telegram Stars
        pass
    
    async def create_payment(self, user_id: int, plan_id: str) -> Dict[str, Any]:
        """Создает платеж для пользователя - теперь через Telegram Stars"""
        plan = PaymentPlans.get_plan(plan_id)
        if not plan:
            raise ValueError(f"Plan {plan_id} not found")
        
        # Платежи теперь обрабатываются через stars_payment_handlers
        return {
            "success": True,
            "message": "Use stars_payment_handlers for payment creation",
            "plan_id": plan_id
        }
    
    async def process_payment_success(self, user_id: int, payment_id: str) -> Dict[str, Any]:
        """Обрабатывает успешный платеж - теперь через Telegram Stars"""
        # Payments now handled directly in stars_payment_handlers
        return {
            "success": False,
            "error": "Payments now handled via Telegram Stars handlers"
        }
    
    async def _apply_payment_benefits(self, user_id: int, plan: PaymentPlan) -> Dict[str, Any]:
        """Применяет бонусы от платежа"""
        from db import add_hearts, grant_access
        
        benefits_applied = []
        
        try:
            if plan.payment_type == PaymentType.HEARTS_PACK:
                # Начисляем сердечки
                hearts_amount = int(plan.amount / 1)  # 1 рубль = 1 сердечко
                await add_hearts(user_id, hearts_amount)
                benefits_applied.append(f"Начислено {hearts_amount} сердечек")
                
            elif plan.payment_type == PaymentType.PREMIUM_SUBSCRIPTION:
                # Предоставляем премиум доступ
                await grant_access(user_id, plan.duration_days)
                benefits_applied.append(f"Премиум доступ на {plan.duration_days} дней")
                
            elif plan.payment_type == PaymentType.DONATION:
                # Для донатов даем небольшой бонус
                await add_hearts(user_id, 10)
                benefits_applied.append("Бонус 10 сердечек за поддержку")
            
            return {
                "benefits": benefits_applied,
                "plan_type": plan.payment_type.value
            }
            
        except Exception as e:
            bot_logger.log_system_error(e, f"Failed to apply payment benefits for user {user_id}")
            raise
    
    async def get_payment_history(self, user_id: int) -> List[Dict[str, Any]]:
        """Получает историю платежей пользователя"""
        # Здесь можно добавить логику получения истории из БД
        return []
    
    async def cancel_payment(self, user_id: int, payment_id: str) -> Dict[str, Any]:
        """Отменяет платеж - не поддерживается для Telegram Stars"""
        return {
            "success": False,
            "error": "Payment cancellation not supported for Telegram Stars"
        }

# Глобальный экземпляр процессора платежей
payment_processor = PaymentProcessor()
