// eslint-disable-next-line @typescript-eslint/no-require-imports
const aws = require('@aws-sdk/client-sesv2');

export default ({ env }) => {
  const isDev = env('NODE_ENV') === 'development';

  return {
    'users-permissions': {
      config: {
        jwt: {
          expiresIn: '4h'
        },
        register: {
          allowedFields: ['candidate']
        }
      }
    },
    email: {
      config: {
        provider: 'nodemailer',
        providerOptions: {
          SES: {
            sesClient: new aws.SESv2Client({
              endpoint: env('LOCALSTACK_ENDPOINT'),
              region: env('AWS_SES_REGION'),
              credentials: {
                accessKeyId: env('AWS_SES_ACCESS_KEY_ID'),
                secretAccessKey: env('AWS_SES_SECRET_ACCESS_KEY')
              }
            }),
            SendEmailCommand: aws.SendEmailCommand
          },
          // max 14 messages per second to comply with AWS SES
          sendingRate: 14
        },
        settings: {
          defaultFrom: env('MAIL_FROM'),
          defaultReplyTo: env('MAIL_REPLY_TO')
        }
      }
    },
    upload: {
      config: {
        provider: 'aws-s3',
        providerOptions: {
          /*
           * The base URL on production uses a dedicated subdomain which is linked to AWS S3 bucket via CNAME DNS record.
           **/
          baseUrl: isDev ? `${env('STATIC_CONTENT_BASE_URL')}/${env('AWS_S3_BUCKET')}` : env('STATIC_CONTENT_BASE_URL'),
          rootPath: env('STATIC_MEDIA_CONTENT_PATH'),
          s3Options: {
            /*
             * In development we use local AWS - LocalStack.
             **/
            endpoint: isDev ? env('LOCALSTACK_ENDPOINT') : undefined,
            /*
             * In development we want to use "Path" style S3 URLs, since
             * Docker services run locally are unable to resolve "Virtual-Hosted" style S3 URLs.
             * https://docs.localstack.cloud/user-guide/aws/s3/#path-style-and-virtual-hosted-style-requests
             *
             **/
            forcePathStyle: isDev,
            credentials: {
              accessKeyId: env('AWS_S3_ACCESS_KEY_ID'),
              secretAccessKey: env('AWS_S3_ACCESS_SECRET')
            },
            region: env('AWS_S3_REGION'),
            params: {
              ACL: 'private',
              Bucket: env('AWS_S3_BUCKET')
            }
          },
          sizeLimit: 20 * 1024 * 1024 // ~20mb in bytes
        },
        actionOptions: {
          upload: {},
          uploadStream: {},
          delete: {}
        }
      }
    },
    'openvaa-admin-tools': {
      enabled: true,
      resolve: './src/plugins/openvaa-admin-tools'
    }
  };
};
