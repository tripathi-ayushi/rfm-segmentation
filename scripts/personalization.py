def assign_action(row):
    if row['churn_prediction'] == 1:
        if row['Segment'] == 'At-Risk':
            return 'Reactivation Email + Big Discount'
        elif row['Segment'] == 'Recent Low-Spenders':
            return 'Limited-Time Discount Offer'
        elif row['Segment'] == 'Loyal Customers':
            return 'Exclusive Reward + Win-Back Message'
        elif row['Segment'] == 'VIP Customers':
            return 'Premium Perk + Retention Call'
    else:
        if row['Segment'] == 'At-Risk':
            return 'Passive Nurture'
        elif row['Segment'] == 'Recent Low-Spenders':
            return 'Upsell: Bundle Offer'
        elif row['Segment'] == 'Loyal Customers':
            return 'Loyalty Bonus + Referral Code'
        elif row['Segment'] == 'VIP Customers':
            return 'VIP Thank You Package'
    return 'General Engagement'

