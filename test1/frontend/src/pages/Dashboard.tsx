import React from 'react';
import { Card, Row, Col, Statistic } from 'antd';
import {
  DollarOutlined,
  ShoppingOutlined,
  PercentageOutlined,
  LineChartOutlined,
} from '@ant-design/icons';
import { useQuery } from '@tanstack/react-query';
import { metricsAPI } from '../services/api';
import dayjs from 'dayjs';

const Dashboard: React.FC = () => {
  const { data: overview, isLoading } = useQuery({
    queryKey: ['dashboard-overview'],
    queryFn: () =>
      metricsAPI.getDashboardOverview({
        account_id: 'default',
        start_date: dayjs().subtract(7, 'day').format('YYYY-MM-DD'),
        end_date: dayjs().format('YYYY-MM-DD'),
      }),
  });

  const data = overview?.data;

  return (
    <div>
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="总花费"
              value={data?.total_spend || 0}
              precision={2}
              prefix={<DollarOutlined />}
              suffix="USD"
              loading={isLoading}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="总销售额"
              value={data?.total_sales || 0}
              precision={2}
              prefix={<ShoppingOutlined />}
              suffix="USD"
              loading={isLoading}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="平均 ACoS"
              value={data?.average_acos || 0}
              precision={2}
              prefix={<PercentageOutlined />}
              suffix="%"
              loading={isLoading}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="平均 ROAS"
              value={data?.average_roas || 0}
              precision={2}
              prefix={<LineChartOutlined />}
              loading={isLoading}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        <Col xs={24} lg={12}>
          <Card title="ACoS 趋势">
            <div style={{ height: 300 }}>
              {/* ECharts 组件将在此渲染 */}
            </div>
          </Card>
        </Col>
        <Col xs={24} lg={12}>
          <Card title="花费分布">
            <div style={{ height: 300 }}>
              {/* ECharts 组件将在此渲染 */}
            </div>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
